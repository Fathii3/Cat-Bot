import time
import streamlit as st
from knowledge.portfolio_data import PORTFOLIO_CONTEXT
from styles import apply_custom_css
from components import (
    ICON,
    show_skeleton,
    show_callout,
    render_sidebar_brand,
    render_top_navbar,
    render_quick_pills,
)
from utils import (
    DEFAULT_MESSAGES,
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
)

# konfigurasi halaman & avatar (fetty)
fetty_AVATAR = "assets/fetty_avatar.svg"
USER_AVATAR = "assets/user_avatar.svg"

st.set_page_config(
    page_title="fetty Assistant",
    page_icon=fetty_AVATAR,
    layout="centered",
    initial_sidebar_state="auto"
)

# tema & gaya
apply_custom_css()

# inisialisasi state
api_keys = load_gemini_keys()
if not api_keys:
    st.error("API key Gemini belum diatur di .streamlit/secrets.toml")
    st.stop()

init_gemini_state(api_keys)
init_session_state()

# identifikasi klien & periksa batas kuota harian
client_ip = get_client_ip()
limit_info = get_rate_limit_info(client_ip)

# sidebar & riwayat chat
with st.sidebar:
    render_sidebar_brand()

    if st.button("Chat Baru", icon=":material/add:", use_container_width=True, type="primary"):
        create_new_session()
        st.toast("Chat baru siap!", icon=":material/check_circle:")
        st.rerun()

    st.markdown('<div class="sidebar-section-title">Riwayat Percakapan</div>', unsafe_allow_html=True)

    session_ids = list(reversed(st.session_state.sessions.keys()))
    total_sessions = len(session_ids)

    for sid in session_ids:
        session = st.session_state.sessions[sid]
        is_active = sid == st.session_state.active_session
        title = session["title"]
        created = session["created"]
        session_icon = ":material/radio_button_checked:" if is_active else ":material/chat_bubble:"

        if total_sessions > 1:
            col_btn, col_save, col_del = st.columns([5, 1, 1], vertical_alignment="center")
        else:
            col_btn, col_save = st.columns([5, 1], vertical_alignment="center")

        with col_btn:
            if st.button(
                title,
                icon=session_icon,
                key=f"session_{sid}",
                use_container_width=True,
                disabled=is_active,
                help=f"Percakapan: {title} ({created})"
            ):
                st.session_state.active_session = sid
                st.toast(f"Pindah ke: {title}", icon=":material/folder_open:")
                st.rerun()

        with col_save:
            txt_data = export_session_txt(session)
            safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
            file_name = f"chat_{safe_title[:18] if safe_title else 'fetty'}.txt"
            st.download_button(
                label="",
                data=txt_data,
                file_name=file_name,
                mime="text/plain",
                icon=":material/download:",
                key=f"dl_{sid}",
                use_container_width=False
            )

        if total_sessions > 1:
            with col_del:
                if st.button("", icon=":material/delete:", key=f"del_{sid}", help="Hapus chat ini", use_container_width=False):
                    deleted_title = delete_session(sid)
                    st.toast(f"Chat \"{deleted_title}\" dihapus", icon=":material/delete:")
                    st.rerun()

    st.markdown(f"""
    <div class="sidebar-footer">
        <span>{ICON["chart"]} {total_sessions} chat tersimpan • Kuota: {limit_info['remaining_questions']}/5</span>
    </div>
    """, unsafe_allow_html=True)

# navbar chat aktif
active_session = get_active_session()
render_top_navbar(active_session)

# bersihkan chat
col_spacer, col_clear = st.columns([8, 2])
with col_clear:
    if st.button("Bersihkan Chat", icon=":material/delete_sweep:", key="clear_chat", use_container_width=True):
        set_active_messages(list(DEFAULT_MESSAGES))
        active_session["title"] = "Chat Baru"
        st.toast("Chat berhasil dibersihkan", icon=":material/check_circle:")
        st.rerun()

# pesan sambutan
has_user_msg = any(m["role"] == "user" for m in get_active_messages())
if not has_user_msg:
    show_callout(
        "Mau tau soal proyek, tech stack, sertifikasi, atau pengalaman Fathi? Langsung ketik di bawah ya, Fetty siap bantu!",
        type="tip",
        title="Hai, selamat datang!"
    )

# riwayat pesan
messages = get_active_messages()
for msg in messages:
    avatar = fetty_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# pintasan topik
render_quick_pills()

# status batas kuota & anti-spam
render_rate_limit_badge(limit_info)

# input chat & respon ai
input_disabled = limit_info["is_daily_limit_reached"]
input_placeholder = (
    "Batas kuota harian habis (5/5 pertanyaan hari ini)"
    if input_disabled
    else "Ketik pertanyaan kamu di sini..."
)
user_input = st.chat_input(input_placeholder, disabled=input_disabled)
prompt_to_send = user_input or st.session_state.pop("pending_pill_prompt", None)

if prompt_to_send:
    # verifikasi proteksi rate limit sebelum memproses pertanyaan
    current_limit = get_rate_limit_info(client_ip)
    if not current_limit["is_allowed"]:
        if current_limit["is_daily_limit_reached"]:
            st.toast("Batas 5 pertanyaan hari ini sudah tercapai.", icon=":material/block:")
            st.rerun()
        elif current_limit["is_cooldown_active"]:
            cooldown_sec = current_limit["cooldown_remaining"]
            st.toast(f"Tunggu jeda {cooldown_sec} detik lagi ya!", icon=":material/timer:")
            countdown_box = st.empty()
            for s in range(cooldown_sec, 0, -1):
                countdown_box.warning(f"Jeda anti-spam: mohon tunggu {s} detik sebelum pesan berikutnya dapat dikirim...")
                time.sleep(1)
            countdown_box.empty()
            st.rerun()

    # catat pertanyaan ke riwayat kuota ip
    record_question(client_ip)

    messages.append({"role": "user", "content": prompt_to_send})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt_to_send)

    # buat judul dari pesan pertama
    if active_session["title"] == "Chat Baru":
        active_session["title"] = generate_title(messages)

    with st.chat_message("assistant", avatar=fetty_AVATAR):
        skeleton_placeholder = st.empty()
        with skeleton_placeholder:
            show_skeleton()

        reply, last_error = generate_fetty_response(
            api_keys=api_keys,
            messages=messages,
            user_input=prompt_to_send,
            portfolio_context=PORTFOLIO_CONTEXT
        )

        skeleton_placeholder.empty()

        if reply:
            st.markdown(reply)
        else:
            err_msg = str(last_error) if last_error else ""
            if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                reply = "Maaf meow, kuota percakapan AI sedang penuh sementara waktu. Tunggu 10-30 detik lalu tanyakan lagi ya!"
            else:
                reply = "Waduh, koneksi ke server AI lagi terganggu nih meow~ Coba refresh halaman atau tanyakan lagi ya!"

            st.markdown(reply)
            show_callout(
                "Sistem AI sedang sibuk atau batas kuota harian tercapai. Silakan coba beberapa saat lagi.",
                type="warning",
                title="Layanan Sedang Sibuk"
            )
            st.toast("Gagal mendapatkan respons, coba lagi ya", icon=":material/warning:")

    messages.append({"role": "assistant", "content": reply})
