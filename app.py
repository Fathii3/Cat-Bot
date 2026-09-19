import time
import importlib
import textwrap
import streamlit as st
import components

# Pastikan modul components selalu tersinkronisasi jika server Streamlit berjalan terus-menerus
if not hasattr(components, "render_welcome_hero") or not hasattr(components, "render_hero_prompt_cards"):
    try:
        importlib.reload(components)
    except Exception:
        pass

from knowledge.portfolio_data import PORTFOLIO_CONTEXT
from styles import apply_custom_css
from components import (
    ICON,
    show_skeleton,
    show_callout,
    render_sidebar_brand,
    render_top_navbar,
    render_welcome_hero,
    render_hero_prompt_cards,
)
from utils import (
    GENAI_AVAILABLE,
    GENAI_ERROR,
    get_default_messages,
    sync_initial_greeting,
    init_session_state,
    get_active_session,
    get_active_messages,
    set_active_messages,
    generate_title,
    create_new_session,
    delete_session,
    export_session_txt,
    load_gemini_keys,
    init_gemini_state,
    generate_fetty_response,
    get_client_ip,
    get_rate_limit_info,
    record_question,
    render_rate_limit_badge,
    get_rate_limit_caption,
)

# 1. Konfigurasi halaman & avatar
fetty_AVATAR = "assets/fetty_avatar.svg"
USER_AVATAR = "assets/user_avatar.svg"

st.set_page_config(
    page_title="Fetty Assistant · Portfolio AI",
    page_icon=fetty_AVATAR,
    layout="centered",
    initial_sidebar_state="auto",
)

# 2. Terapkan custom CSS (Gemini style layout: lock window, scroll chat only)
apply_custom_css()

# 3. Verifikasi dependensi AI
if not GENAI_AVAILABLE:
    st.error(
        f"**Modul AI (`google-genai`) belum siap di server:** `{GENAI_ERROR}`\n\n"
        "**Cara Memperbaiki di Streamlit Cloud:**\n"
        "1. Masuk ke dashboard Streamlit Cloud -> klik **Manage app** (kanan bawah).\n"
        "2. Masuk ke **Settings** > **General** > pastikan **Python version** diatur ke **3.10** atau **3.11**.\n"
        "3. Klik ikon titik tiga ⋮ pada menu Manage app lalu pilih **Rebuild with clear cache**."
    )
    st.stop()

api_keys = load_gemini_keys()
if not api_keys:
    st.error("API key Gemini belum diatur di .streamlit/secrets.toml")
    st.stop()

init_gemini_state(api_keys)

# 4. Deteksi bahasa awal dari query params & inisialisasi state sesi
url_lang = st.query_params.get("lang", "").lower()
initial_is_en = url_lang not in ("id", "ina", "indonesia")
init_session_state(is_en=initial_is_en)

# 5. Identifikasi klien & status batas kuota harian
client_ip = get_client_ip()
limit_info = get_rate_limit_info(client_ip)

# 6. Sidebar: Brand, Bahasa, Riwayat Chat, dan Pintasan
with st.sidebar:
    render_sidebar_brand()

    default_lang = "English" if initial_is_en else "Indonesia"
    lang_choice = st.segmented_control(
        "Language",
        options=["English", "Indonesia"],
        default=default_lang,
        label_visibility="collapsed",
        key="app_lang",
    )
    current_lang = lang_choice or st.session_state.get("prev_lang") or default_lang
    is_en = current_lang != "Indonesia"

    if "prev_lang" in st.session_state and st.session_state["prev_lang"] != current_lang:
        toast_msg = (
            "Language changed to English 🇬🇧"
            if is_en
            else "Bahasa berhasil diubah ke Indonesia 🇮🇩"
        )
        st.toast(toast_msg, icon=":material/translate:")
    st.session_state["prev_lang"] = current_lang

    active_session = get_active_session()
    sync_initial_greeting(active_session, is_en=is_en)

    new_chat_lbl = "New Chat" if is_en else "Chat Baru"
    if st.button(new_chat_lbl, icon=":material/add:", use_container_width=True, type="primary"):
        create_new_session(is_en=is_en)
        st.toast("New chat ready!" if is_en else "Chat baru siap!", icon=":material/check_circle:")
        st.rerun()

    history_title = "Chat History" if is_en else "Riwayat Percakapan"
    st.markdown(f'<div class="sidebar-section-title">{history_title}</div>', unsafe_allow_html=True)

    session_ids = list(reversed(st.session_state.sessions.keys()))
    total_sessions = len(session_ids)

    for sid in session_ids:
        session = st.session_state.sessions[sid]
        is_active = sid == st.session_state.active_session
        title = session["title"]
        created = session["created"]
        session_icon = ":material/radio_button_checked:" if is_active else ":material/chat_bubble:"

        col_btn, col_opt = st.columns([5, 1], vertical_alignment="center")

        with col_btn:
            if st.button(
                title,
                icon=session_icon,
                key=f"session_{sid}",
                use_container_width=True,
                disabled=is_active,
                help=f"{title} ({created})"
            ):
                st.session_state.active_session = sid
                st.rerun()

        with col_opt:
            with st.popover("", icon=":material/more_vert:", help="Session options" if is_en else "Opsi sesi"):
                txt_data = export_session_txt(session)
                safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
                file_name = f"chat_{safe_title[:18] if safe_title else 'fetty'}.txt"
                st.download_button(
                    label="Download .txt" if is_en else "Unduh .txt",
                    data=txt_data,
                    file_name=file_name,
                    mime="text/plain",
                    icon=":material/download:",
                    key=f"dl_{sid}",
                    use_container_width=True
                )
                if total_sessions > 1:
                    del_lbl = "Delete Chat" if is_en else "Hapus Chat"
                    if st.button(del_lbl, icon=":material/delete:", key=f"del_{sid}", use_container_width=True):
                        deleted_title = delete_session(sid)
                        del_toast = f'Chat "{deleted_title}" deleted' if is_en else f'Chat "{deleted_title}" dihapus'
                        st.toast(del_toast, icon=":material/delete:")
                        st.rerun()

    footer_lbl = (
        f"{total_sessions} chats saved • Quota: {limit_info['remaining_questions']}/5"
        if is_en
        else f"{total_sessions} chat tersimpan • Kuota: {limit_info['remaining_questions']}/5"
    )
    html_footer = textwrap.dedent(f"""
    <div class="sidebar-footer">
        <span>{ICON["chart"]} {footer_lbl}</span>
    </div>
    """).strip()
    st.markdown(html_footer, unsafe_allow_html=True)

# 7. Header Bar (Fixed / Sticky di bagian atas viewport)
active_session = get_active_session()

with st.container(key="app_header"):
    render_top_navbar(active_session, is_en=is_en, limit_info=limit_info)

# 8. Siapkan Input Chat & Tangkap Submit Pengguna
is_quota_exhausted = limit_info["is_daily_limit_reached"]
is_cooldown = limit_info["is_cooldown_active"]
input_disabled = is_quota_exhausted

if is_quota_exhausted:
    input_placeholder = "Daily quota reached (5/5 questions today)" if is_en else "Batas kuota harian habis (5/5 pertanyaan hari ini)"
elif is_cooldown:
    cd_val = limit_info["cooldown_remaining"]
    input_placeholder = f"Anti-spam active (wait {cd_val}s)..." if is_en else f"Jeda anti-spam (tunggu {cd_val}d)..."
else:
    input_placeholder = "Ask anything about Fathi's projects, tech stack..." if is_en else "Ketik pertanyaan kamu seputar portofolio Fathi..."

user_input = st.chat_input(input_placeholder, disabled=input_disabled)
prompt_to_send = user_input or st.session_state.pop("pending_pill_prompt", None)

# 9. Wadah Percakapan Chat (Scrollable Area — Satu-satunya yang ber-scroll)
messages = get_active_messages()
has_user_msg = any(m["role"] == "user" for m in messages)

with st.container(key="chat_scroll_container", height=540, border=False, autoscroll=True):
    # Banner status kuota jika habis atau dalam jeda cooldown
    if limit_info["is_daily_limit_reached"] or limit_info["is_cooldown_active"]:
        render_rate_limit_badge(limit_info, is_en=is_en)

    # Jika sesi baru tanpa pertanyaan pengunjung: Tampilkan Gemini-style Welcome Hero
    if not has_user_msg and not prompt_to_send:
        render_welcome_hero(is_en=is_en)
        render_hero_prompt_cards(is_en=is_en)
    else:
        # Render seluruh riwayat pesan
        for msg in messages:
            avatar = fetty_AVATAR if msg["role"] == "assistant" else USER_AVATAR
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # Tangani pengiriman pesan baru di dalam container yang sama
    if prompt_to_send:
        # Verifikasi cooldown tanpa memblokir server
        current_limit = get_rate_limit_info(client_ip)
        if not current_limit["is_allowed"]:
            if current_limit["is_daily_limit_reached"]:
                st.toast("Daily limit of 5 questions reached." if is_en else "Batas 5 pertanyaan hari ini tercapai.", icon=":material/block:")
                st.rerun()
            elif current_limit["is_cooldown_active"]:
                cd_rem = current_limit["cooldown_remaining"]
                st.toast(
                    f"Please wait {cd_rem}s before next prompt!" if is_en else f"Mohon tunggu jeda {cd_rem} detik ya!",
                    icon=":material/timer:"
                )
                st.session_state["pending_pill_prompt"] = prompt_to_send
                st.rerun()

        # Catat pertanyaan ke riwayat kuota IP
        record_question(client_ip)

        # Tambahkan pesan user ke state & tampilkan langsung di container
        messages.append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt_to_send)

        # Buat judul dari pesan pertama
        if active_session["title"] in ("Chat Baru", "New Chat"):
            active_session["title"] = generate_title(messages)

        # Tampilkan respons asisten dengan thinking skeleton
        with st.chat_message("assistant", avatar=fetty_AVATAR):
            skeleton_placeholder = st.empty()
            with skeleton_placeholder:
                show_skeleton(is_en=is_en)

            reply, last_error = generate_fetty_response(
                api_keys=api_keys,
                messages=messages,
                user_input=prompt_to_send,
                portfolio_context=PORTFOLIO_CONTEXT,
                is_en=is_en
            )

            skeleton_placeholder.empty()

            if reply:
                st.markdown(reply)
            else:
                err_msg = str(last_error) if last_error else ""
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    reply = (
                        "Sorry meow, AI conversation quota is temporarily full. Please wait 10-30 seconds and try again!"
                        if is_en
                        else "Maaf meow, kuota percakapan AI sedang penuh sementara waktu. Tunggu 10-30 detik lalu tanyakan lagi ya!"
                    )
                else:
                    reply = (
                        "Oops, connection to AI server had a hiccup meow~ Please refresh or try again!"
                        if is_en
                        else "Waduh, koneksi ke server AI lagi terganggu nih meow~ Coba refresh halaman atau tanyakan lagi ya!"
                    )

                st.markdown(reply)
                busy_text = (
                    "AI service is currently busy. Please try again shortly."
                    if is_en
                    else "Sistem AI sedang sibuk. Silakan coba beberapa saat lagi."
                )
                busy_title = "Service Busy" if is_en else "Layanan Sedang Sibuk"
                show_callout(busy_text, type="warning", title=busy_title)
                st.toast("Failed to get response, please try again" if is_en else "Gagal mendapatkan respons, coba lagi ya", icon=":material/warning:")

        messages.append({"role": "assistant", "content": reply})

    # Spacer bawah di akhir kontainer agar pesan terbawah tidak pernah terpotong oleh input melayang
    st.markdown(
        '<div class="chat-bottom-spacer" style="height: 140px; min-height: 140px; width: 100%; display: block;">&nbsp;</div>',
        unsafe_allow_html=True
    )

