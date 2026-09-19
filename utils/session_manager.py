from datetime import datetime, timedelta, timezone
import streamlit as st

WIB = timezone(timedelta(hours=7))

def get_now_wib_str() -> str:
    """ambil waktu saat ini dalam format WIB."""
    return f"{datetime.now(WIB).strftime('%d/%m %H:%M')} WIB"

def get_default_messages(is_en: bool = True) -> list:
    """ambil pesan pembuka sesuai bahasa (gaya natural tech companion)."""
    content = (
        "Meow! Hey there, I'm Fetty — Fathi's AI companion 🐾\n\nCurious about his engineering projects, tech stack, or full-stack journey? Ask me anything, or tap one of the quick prompts below!"
        if is_en
        else "Halo meow! Aku Fetty, asisten AI Fathi Fadhil 🐾\n\nMau kepoin proyek unggulan, cara kerja (workflow), atau tech stack Fathi? Tanya apa aja, Fetty siap bantu!"
    )
    return [{"role": "assistant", "content": content}]

DEFAULT_MESSAGES = get_default_messages(is_en=True)

def sync_initial_greeting(session: dict, is_en: bool):
    """perbarui pesan pembuka jika belum ada percakapan user."""
    msgs = session.get("messages", [])
    if len(msgs) == 1 and msgs[0].get("role") == "assistant":
        msgs[0]["content"] = get_default_messages(is_en)[0]["content"]
        if session.get("title") in ("New Chat", "Chat Baru"):
            session["title"] = "New Chat" if is_en else "Chat Baru"

def init_session_state(is_en: bool = True):
    """inisialisasi riwayat chat di memori sesi."""
    if "sessions" not in st.session_state:
        first_id = "chat_1"
        st.session_state.sessions = {
            first_id: {
                "title": "New Chat" if is_en else "Chat Baru",
                "messages": get_default_messages(is_en),
                "created": get_now_wib_str()
            }
        }
        st.session_state.active_session = first_id
        st.session_state.session_counter = 1

def get_active_session() -> dict:
    """ambil sesi chat aktif."""
    return st.session_state.sessions[st.session_state.active_session]

def get_active_messages() -> list:
    """ambil pesan dari sesi aktif."""
    return st.session_state.sessions[st.session_state.active_session]["messages"]

def set_active_messages(msgs: list):
    """simpan pesan ke sesi aktif."""
    st.session_state.sessions[st.session_state.active_session]["messages"] = msgs

def generate_title(messages: list) -> str:
    """buat judul dari pesan pertama."""
    for msg in messages:
        if msg["role"] == "user":
            text = msg["content"].strip()
            return text[:26] + "..." if len(text) > 26 else text
    return "New Chat"

def create_new_session(is_en: bool = True) -> str:
    """buat sesi chat baru."""
    st.session_state.session_counter += 1
    new_id = f"chat_{st.session_state.session_counter}"
    st.session_state.sessions[new_id] = {
        "title": "New Chat" if is_en else "Chat Baru",
        "messages": get_default_messages(is_en),
        "created": get_now_wib_str()
    }
    st.session_state.active_session = new_id
    return new_id

def delete_session(sid: str) -> str:
    """hapus sesi chat."""
    deleted_title = st.session_state.sessions[sid]["title"]
    del st.session_state.sessions[sid]
    if st.session_state.active_session == sid:
        st.session_state.active_session = list(st.session_state.sessions.keys())[-1]
    return deleted_title

def export_session_txt(session: dict) -> str:
    """format percakapan sesi menjadi teks terstruktur untuk diunduh."""
    title = session.get("title", "Chat")
    created = session.get("created", "-")
    lines = [
        "========================================",
        "RIWAYAT PERCAKAPAN - FETTY ASSISTANT",
        f"Sesi   : {title}",
        f"Waktu  : {created}",
        "========================================\n",
    ]
    for msg in session.get("messages", []):
        role = "Pengunjung" if msg.get("role") == "user" else "Fetty"
        content = msg.get("content", "").strip()
        lines.append(f"[{role}]:\n{content}\n")

    lines.append("========================================")
    lines.append("Portofolio Fathi Fadhil (fathifadhil.me)")
    lines.append("========================================")
    return "\n".join(lines)
