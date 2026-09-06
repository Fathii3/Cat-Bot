import streamlit as st
from streamlit_local_storage import LocalStorage
from google import genai
from google.genai import types
import json
from knowledge.portfolio_data import PORTFOLIO_CONTEXT

# 1. Konfigurasi Halaman & Styling
st.set_page_config(page_title="Neko Assistant", page_icon="🐱", layout="centered")

st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem; padding-left: 1rem; padding-right: 1rem;}
    .stChatMessage {border-radius: 12px; margin-bottom: 6px;}
</style>
""", unsafe_allow_html=True)

# 2. Inisialisasi Gemini Client
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    st.error("API Key Gemini belum diatur di secrets.")
    st.stop()

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=GEMINI_KEY)

# 3. Inisialisasi LocalStorage
ls = LocalStorage()

# 4. Load chat history dari localStorage browser
DEFAULT_MESSAGES = [
    {"role": "assistant", "content": "Halo meow! 🐾 Aku Neko, asisten Fathi Fadhil. Mau tanya seputar proyek Flutter, Full Stack, atau keahlian Fathi?"}
]

if "messages" not in st.session_state:
    saved = ls.getItem("neko_chat_history")
    if saved:
        try:
            st.session_state.messages = json.loads(saved) if isinstance(saved, str) else saved
        except Exception:
            st.session_state.messages = DEFAULT_MESSAGES
    else:
        st.session_state.messages = DEFAULT_MESSAGES

# 5. Tombol Clear Chat
col1, col2 = st.columns([8, 2])
with col2:
    if st.button("🗑️", help="Hapus riwayat chat", use_container_width=True):
        st.session_state.messages = DEFAULT_MESSAGES
        ls.deleteItem("neko_chat_history")
        st.rerun()

# 6. Render Riwayat Chat
for msg in st.session_state.messages:
    avatar = "🐱" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 7. Handle Input User
user_input = st.chat_input("Tanya proyek atau keahlian Fathi...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Setup Prompt & Parameter Gemini
    system_instruction = f"""
Kamu adalah Neko, asisten AI kucing pintar untuk portofolio Fathi Fadhil (fathifadhil.me).
Gunakan rujukan mutlak berikut:
{PORTFOLIO_CONTEXT}

Aturan:
- Ramah, solutif, sesekali gunakan gaya kucing (meow/🐾).
- Jawab maksimal 3-4 kalimat singkat padat.
- Hanya jawab seputar profil, keahlian, dan proyek Fathi. Tolak topik lain dengan sopan.
"""

    chat_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.2,
        top_p=0.95,
        top_k=20
    )

    with st.chat_message("assistant", avatar="🐱"):
        with st.spinner("Neko sedang berpikir... 🐾"):
            try:
                history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
                prompt = f"RIWAYAT PERCAKAPAN:\n{history_text}\n\nPERTANYAAN USER:\n{user_input}"

                response = st.session_state.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config=chat_config
                )
                reply = response.text
            except Exception as e:
                reply = f"Maaf meow, terjadi kesalahan teknis: {e}"

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Save ke localStorage browser setiap ada pesan baru
    ls.setItem("neko_chat_history", json.dumps(st.session_state.messages, ensure_ascii=False))
