from datetime import datetime
import streamlit as st

DEFAULT_MESSAGES = [
    {
        "role": "assistant",
        "content": "Halo meow! Aku Fetty, asisten Fathi Fadhil. Mau tanya seputar proyek, keahlian, atau tech stack Fathi? Tanya aja!"
    }
]

def init_session_state():
    """Inisialisasi riwayat chat."""
    if "sessions" not in st.session_state:
        first_id = "chat_1"
        st.session_state.sessions = {
            first_id: {
                "title": "Chat Baru",
                "messages": list(DEFAULT_MESSAGES),
                "created": datetime.now().strftime("%d/%m %H:%M")
            }
        }
        st.session_state.active_session = first_id
        st.session_state.session_counter = 1

def get_active_session() -> dict:
    """Ambil sesi chat aktif."""
    return st.session_state.sessions[st.session_state.active_session]

def get_active_messages() -> list:
    """Ambil pesan dari sesi aktif."""
    return st.session_state.sessions[st.session_state.active_session]["messages"]

def set_active_messages(msgs: list):
    """Simpan pesan ke sesi aktif."""
    st.session_state.sessions[st.session_state.active_session]["messages"] = msgs

def generate_title(messages: list) -> str:
    """Buat judul dari pesan pertama."""
    for msg in messages:
        if msg["role"] == "user":
            text = msg["content"].strip()
            return text[:26] + "..." if len(text) > 26 else text
    return "Chat Baru"

def create_new_session() -> str:
    """Buat sesi chat baru."""
    st.session_state.session_counter += 1
    new_id = f"chat_{st.session_state.session_counter}"
    st.session_state.sessions[new_id] = {
        "title": "Chat Baru",
        "messages": list(DEFAULT_MESSAGES),
        "created": datetime.now().strftime("%d/%m %H:%M")
    }
    st.session_state.active_session = new_id
    return new_id

def delete_session(sid: str) -> str:
    """Hapus sesi chat."""
    deleted_title = st.session_state.sessions[sid]["title"]
    del st.session_state.sessions[sid]
    if st.session_state.active_session == sid:
        st.session_state.active_session = list(st.session_state.sessions.keys())[-1]
    return deleted_title
