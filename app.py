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
if not GENAI_AVAILABLE:
    st.error(
        f"**Modul AI (`google-genai`) belum siap di server:** `{GENAI_ERROR}`\n\n"
        "**Cara Memperbaiki di Streamlit Cloud:**\n"
        "1. Masuk ke dashboard Streamlit Cloud -> klik **Manage app** (kanan bawah).\n"
        "2. Masuk ke **Settings** > **General** > pastikan **Python version** diatur ke **3.10** atau **3.11** (karena `google-genai` butuh Python >= 3.10).\n"
        "3. Klik ikon titik tiga ⋮ pada menu Manage app lalu pilih **Rebuild with clear cache**."
    )
    st.stop()

api_keys = load_gemini_keys()
if not api_keys:
    st.error("API key Gemini belum diatur di .streamlit/secrets.toml")
    st.stop()

init_gemini_state(api_keys)
init_session_state(is_en=True)

# identifikasi klien & periksa batas kuota harian
client_ip = get_client_ip()
limit_info = get_rate_limit_info(client_ip)

# sidebar & riwayat chat
with st.sidebar:
    render_sidebar_brand()

    # mode 2 bahasa (default: English, auto-detect dari url param ?lang=id)
    url_lang = st.query_params.get("lang", "").lower()
    default_lang = "Indonesia" if url_lang in ("id", "ina", "indonesia") else "English"

    lang_choice = st.segmented_control(
        "Language",
        options=["English", "Indonesia"],
        default=default_lang,
        label_visibility="collapsed",
        key="app_lang",
    )
    current_lang = lang_choice or st.session_state.get("prev_lang") or default_lang
    is_en = current_lang != "Indonesia"

    # notifikasi pergantian bahasa
    if "prev_lang" in st.session_state and st.session_state["prev_lang"] != current_lang:
        toast_msg = (
            "Language changed to English 🇬🇧"
            if is_en
            else "Bahasa berhasil diubah ke Indonesia 🇮🇩"
        )
        st.toast(toast_msg, icon=":material/translate:")
    st.session_state["prev_lang"] = current_lang

    # perbarui pesan pembuka sesi aktif jika user belum mengirim pesan
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
                help=f"Percakapan: {title} ({created})"
            ):
                st.session_state.active_session = sid
                st.toast(f"Pindah ke: {title}", icon=":material/folder_open:")
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

    footer_lbl = f"{total_sessions} chats saved • Quota: {limit_info['remaining_questions']}/5" if is_en else f"{total_sessions} chat tersimpan • Kuota: {limit_info['remaining_questions']}/5"
    st.markdown(f"""
    <div class="sidebar-footer">
        <span>{ICON["chart"]} {footer_lbl}</span>
    </div>
    """, unsafe_allow_html=True)

# navbar chat aktif
active_session = get_active_session()
render_top_navbar(active_session, is_en=is_en)

# bersihkan chat
col_spacer, col_clear = st.columns([8, 2])
with col_clear:
    clear_lbl = "Clear Chat" if is_en else "Bersihkan Chat"
    if st.button(clear_lbl, icon=":material/delete_sweep:", key="clear_chat", use_container_width=True):
        set_active_messages(get_default_messages(is_en=is_en))
        active_session["title"] = "New Chat" if is_en else "Chat Baru"
        st.toast("Chat cleared" if is_en else "Chat berhasil dibersihkan", icon=":material/check_circle:")
        st.rerun()

# pesan sambutan
has_user_msg = any(m["role"] == "user" for m in get_active_messages())
if not has_user_msg:
    welcome_msg = (
        "Want to explore Fathi's projects, tech stack, certifications, or work experience? Ask below, Fetty is ready to help!"
        if is_en
        else "Mau tau soal proyek, tech stack, sertifikasi, atau pengalaman Fathi? Langsung ketik di bawah ya, Fetty siap bantu!"
    )
    welcome_title = "Hello, welcome!" if is_en else "Hai, selamat datang!"
    show_callout(welcome_msg, type="tip", title=welcome_title)

# riwayat pesan
messages = get_active_messages()
for msg in messages:
    avatar = fetty_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# pintasan topik
render_quick_pills(is_en=is_en)

# status batas kuota & anti-spam
render_rate_limit_badge(limit_info, is_en=is_en)

# input chat & respon ai
input_disabled = limit_info["is_daily_limit_reached"]
input_placeholder = (
    ("Daily quota limit reached (5/5 questions today)" if is_en else "Batas kuota harian habis (5/5 pertanyaan hari ini)")
    if input_disabled
    else ("Ask anything about Fathi's work..." if is_en else "Ketik pertanyaan kamu di sini...")
)
user_input = st.chat_input(input_placeholder, disabled=input_disabled)
prompt_to_send = user_input or st.session_state.pop("pending_pill_prompt", None)

if prompt_to_send:
    # verifikasi proteksi rate limit sebelum memproses pertanyaan
    current_limit = get_rate_limit_info(client_ip)
    if not current_limit["is_allowed"]:
        if current_limit["is_daily_limit_reached"]:
            st.toast("Daily limit of 5 questions reached." if is_en else "Batas 5 pertanyaan hari ini sudah tercapai.", icon=":material/block:")
            st.rerun()
        elif current_limit["is_cooldown_active"]:
            cooldown_sec = current_limit["cooldown_remaining"]
            st.toast(f"Please wait {cooldown_sec}s cooldown!" if is_en else f"Tunggu jeda {cooldown_sec} detik lagi ya!", icon=":material/timer:")
            countdown_box = st.empty()
            for s in range(cooldown_sec, 0, -1):
                cd_text = f"Anti-spam cooldown: please wait {s}s before sending next message..." if is_en else f"Jeda anti-spam: mohon tunggu {s} detik sebelum pesan berikutnya dapat dikirim..."
                countdown_box.warning(cd_text)
                time.sleep(1)
            countdown_box.empty()
            st.rerun()

    # catat pertanyaan ke riwayat kuota ip
    record_question(client_ip)

    messages.append({"role": "user", "content": prompt_to_send})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt_to_send)

    # buat judul dari pesan pertama
    if active_session["title"] in ("Chat Baru", "New Chat"):
        active_session["title"] = generate_title(messages)

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
                "AI service is currently busy or daily limit has been reached. Please try again shortly."
                if is_en
                else "Sistem AI sedang sibuk atau batas kuota harian tercapai. Silakan coba beberapa saat lagi."
            )
            busy_title = "Service Busy" if is_en else "Layanan Sedang Sibuk"
            show_callout(busy_text, type="warning", title=busy_title)
            st.toast("Failed to get response, please try again" if is_en else "Gagal mendapatkan respons, coba lagi ya", icon=":material/warning:")

    messages.append({"role": "assistant", "content": reply})
