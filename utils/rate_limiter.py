"""modul pembatasan frekuensi pesan (rate limiting) dan anti-spam berbasis ip."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import threading
import time
import streamlit as st
from components.icons import ICON

WIB = timezone(timedelta(hours=7))
DAILY_LIMIT = 5
COOLDOWN_SECONDS = 30
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "rate_limit.json"

_file_lock = threading.Lock()


def _get_today_wib() -> str:
    """tanggal hari ini berdasarkan zona waktu indonesia (WIB / UTC+7)."""
    return datetime.now(WIB).date().isoformat()


def get_client_ip() -> str:
    """ekstraksi ip pengunjung secara akurat dari konteks streamlit / reverse proxy."""
    try:
        headers = getattr(st.context, "headers", None) or {}
        # x-forwarded-for dapat berupa daftar ip 'klien, proxy1, proxy2'
        forwarded = headers.get("x-forwarded-for") or headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
            if ip:
                return ip

        cf_ip = headers.get("cf-connecting-ip") or headers.get("CF-Connecting-IP")
        if cf_ip:
            return cf_ip.strip()

        real_ip = headers.get("x-real-ip") or headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()

        ip_addr = getattr(st.context, "ip_address", None)
        if ip_addr:
            return str(ip_addr).strip()
    except Exception:
        pass

    return "127.0.0.1"


def _load_all_records() -> dict:
    """baca catatan kuota dari berkas json secara aman."""
    if not DATA_FILE.exists():
        return {}
    try:
        with _file_lock:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return {}


def _save_all_records(data: dict):
    """simpan catatan kuota ke berkas json secara aman."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with _file_lock:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
    except Exception:
        pass


def get_rate_limit_info(ip: str) -> dict:
    """periksa status batas harian dan jeda cooldown untuk ip tertentu."""
    today_str = _get_today_wib()
    records = _load_all_records()
    user_record = records.get(ip, {})

    # reset kuota jika tanggal berubah
    record_date = user_record.get("date")
    if record_date != today_str:
        count = 0
        last_time = 0.0
    else:
        count = int(user_record.get("count", 0))
        last_time = float(user_record.get("last_timestamp", 0.0))

    now = time.time()
    elapsed = now - last_time if last_time > 0 else 9999.0
    cooldown_remaining = max(0, int(COOLDOWN_SECONDS - elapsed)) if elapsed < COOLDOWN_SECONDS else 0

    remaining_questions = max(0, DAILY_LIMIT - count)
    is_daily_limit_reached = count >= DAILY_LIMIT
    is_cooldown_active = cooldown_remaining > 0

    is_allowed = (not is_daily_limit_reached) and (not is_cooldown_active)

    reason = "ok"
    if is_daily_limit_reached:
        reason = "daily_limit"
    elif is_cooldown_active:
        reason = "cooldown"

    return {
        "ip": ip,
        "date": today_str,
        "count": count,
        "limit": DAILY_LIMIT,
        "remaining_questions": remaining_questions,
        "is_daily_limit_reached": is_daily_limit_reached,
        "cooldown_remaining": cooldown_remaining,
        "is_cooldown_active": is_cooldown_active,
        "is_allowed": is_allowed,
        "reason": reason,
    }


def record_question(ip: str):
    """catat pertanyaan baru: tambahkan hitungan hari ini dan perbarui timestamp terakhir."""
    today_str = _get_today_wib()
    records = _load_all_records()
    user_record = records.get(ip, {})

    if user_record.get("date") != today_str:
        count = 1
    else:
        count = int(user_record.get("count", 0)) + 1

    records[ip] = {
        "date": today_str,
        "count": count,
        "last_timestamp": time.time(),
    }
    _save_all_records(records)


def render_rate_limit_badge(info: dict, is_en: bool = True):
    """tampilkan indikator kuota dan status jeda anti-spam."""
    remaining = info["remaining_questions"]
    limit = info["limit"]
    cooldown = info["cooldown_remaining"]

    if info["is_daily_limit_reached"]:
        text = (
            f"<strong>Daily Limit Reached ({limit}/{limit})</strong>: Your IP question quota is exhausted for today. Please come back tomorrow!"
            if is_en
            else f"<strong>Batas Harian Tercapai ({limit}/{limit})</strong>: Kuota pertanyaan untuk alamat IP kamu sudah habis hari ini. Silakan kembali lagi besok ya!"
        )
        st.markdown(
            f"""
            <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; color: #991b1b; display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-flex; align-items: center; color: #dc2626;">{ICON["alert"]}</span>
                <span>{text}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif cooldown > 0:
        cd_msg = (
            f"Anti-spam cooldown: please wait <strong>{cooldown}s</strong> before sending the next message."
            if is_en
            else f"Jeda anti-spam: tunggu <strong>{cooldown} detik</strong> sebelum mengirim pesan berikutnya."
        )
        quota_msg = (
            f"Remaining quota: {remaining}/{limit}"
            if is_en
            else f"Sisa kuota: {remaining}/{limit}"
        )
        st.markdown(
            f"""
            <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; font-size: 13px; color: #92400e; display: flex; flex-direction: column; gap: 6px;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="display: inline-flex; align-items: center; color: #d97706;">{ICON["hourglass"]}</span>
                        <span>{cd_msg}</span>
                    </div>
                    <span style="font-size: 11px; background: #fef3c7; border: 1px solid #fcd34d; padding: 2px 8px; border-radius: 12px; font-weight: 600;">{quota_msg}</span>
                </div>
                <div style="width: 100%; height: 4px; background: #fde68a; border-radius: 2px; overflow: hidden;">
                    <div style="width: {(cooldown / COOLDOWN_SECONDS) * 100}%; height: 100%; background: #d97706; transition: width 1s linear;"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        spam_msg = (
            "Anti-spam active (30s cooldown)"
            if is_en
            else "Anti-spam aktif (jeda 30 detik)"
        )
        daily_msg = (
            f"Daily quota: <strong>{remaining}/{limit}</strong> questions"
            if is_en
            else f"Kuota harian: <strong>{remaining}/{limit}</strong> pertanyaan"
        )
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: #64748b; padding: 4px 8px; margin-bottom: 4px;">
                <span style="display: inline-flex; align-items: center; gap: 4px;">{ICON["shield"]} {spam_msg}</span>
                <span>{daily_msg}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
