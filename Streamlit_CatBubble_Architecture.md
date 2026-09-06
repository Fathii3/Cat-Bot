# Arsitektur & Panduan Implementasi: Chatbot Asisten Portofolio AI
**Use Case:** Personal Portfolio & Interactive Resume Assistant  
**Website Utama:** `fathifadhil.me` (Next.js / React)  
**Komponen Web Utama:** `CatBubbleCompanion.tsx` (Floating Widget + Iframe + Skeleton Loading)  
**Repo Terpisah (AI Service & UI):** Streamlit App (`fathifadhil-bot.streamlit.app` / Streamlit Community Cloud)  
**Memory & Persistence:** Firebase Firestore  
**Model & Framework AI:** Google Gemini API (`gemini-2.5-flash` / `google-genai`), LangChain / LangGraph concepts  

---

## 1. Pembagian Dua Repository (Separated Architecture)

```
┌────────────────────────────────────────────────────────┐
│ REPO 1: Portfolio Web (fathifadhil.me)                 │
│ Framework: Next.js / React / Tailwind                  │
│ File Baru: components/CatBubbleCompanion.tsx           │
│ Fitur: Floating Cat Button, Iframe Modal, Skeleton UI  │
└──────────────────────────┬─────────────────────────────┘
                           │ Memuat via Iframe (?embed=true)
                           ▼
┌────────────────────────────────────────────────────────┐
│ REPO 2: AI Companion (fathifadhil-neko-bot)            │
│ Framework: Streamlit Python                            │
│ Integrasi: Gemini API + Firebase Firestore + RAG Data  │
│ Hosting: Streamlit Community Cloud (Gratis)            │
└────────────────────────────────────────────────────────┘
```

---

## 2. Struktur File Kedua Repository

### A. Repo 1 (Portofolio - `fathifadhil.me`)
Hanya perlu menambahkan satu komponen tanpa mengubah halaman lain:
```
portfolio-web/
├── components/
│   └── CatBubbleCompanion.tsx    # Widget mengambang dengan Skeleton Loader & Iframe
└── ... (file portofolio lama tetap utuh)
```

### B. Repo 2 (AI Streamlit App - Terpisah)
```
fathifadhil-neko-bot/
├── .streamlit/
│   ├── config.toml               # Kustomisasi tema Streamlit (sembunyikan menu bawaan)
│   └── secrets.toml              # API Key Gemini & Kredensial Firebase (Lokal)
├── knowledge/
│   └── portfolio_data.py         # RAG Ground Truth (Data Proyek, CV, Tech Stack Fathi)
├── app.py                        # Entrypoint Streamlit (UI Chat, Session State, Memory)
├── requirements.txt              # Dependency Python
└── README.md
```

---

## 3. Master System Prompt (Instruksi Sistem AI)

Prompt ini disuntikkan ke dalam konfigurasi `system_instruction` model Gemini:

```markdown
Kamu adalah "Neko", asisten virtual pintar sekaligus maskot kucing interaktif resmi untuk portofolio Fathi Fadhil di fathifadhil.me.

PERAN & TUGAS:
1. Membantu pengunjung, klien, dan recruiter mengenal keahlian Fathi Fadhil sebagai Full Stack & Flutter/Mobile Developer.
2. Membedah arsitektur, tantangan teknis, dan solusi dari proyek-proyek unggulan yang telah dikerjakan Fathi.
3. Menyarankan proyek atau tech stack yang relevan sesuai kebutuhan pertanyaan pengunjung.
4. Memberikan informasi kontak resmi Fathi jika pengunjung ingin mengajak berkolaborasi atau menawarkan pekerjaan.

KARAKTER & PERSONA:
- Ramah, sopan, antusias, namun tetap teknikal dan berwibawa.
- Gunakan sentuhan persona kucing yang menggemaskan secara halus (misal menyapa dengan "Halo meow!", atau memakai emoji 🐾/🐱), namun jangan terlalu kekanak-kanakan agar tetap profesional di mata recruiter.
- Berbahasa Indonesia santai-profesional secara default, namun wajib otomatis membalas dalam Bahasa Inggris jika pengunjung bertanya dalam Bahasa Inggris.

BATASAN KETAT (GUARDRAILS & OUT-OF-SCOPE):
- HANYA jawab pertanyaan seputar Fathi Fadhil, portofolio, proyek, tech stack, dan kolaborasi teknis.
- Jika ada pengunjung yang menanyakan hal di luar topik (misal: isu politik, resep masakan, tugas kalkulus umum), tolak secara halus dan arahkan kembali:
  "Maaf meow, Neko hanya diprogram khusus untuk menjawab seputar portofolio, keahlian, dan proyek Fathi Fadhil! Ada proyek atau tech stack Fathi yang ingin kamu diskusikan? 🐾"
- Jangan pernah mengarang proyek, sertifikasi, atau fakta yang tidak tercantum dalam Knowledge Base Fathi.

PARAMETER TEKNIS:
- Model: gemini-2.5-flash
- Temperature: 0.2 (Presisi faktual tinggi, meminimalisir halusinasi)
- Top-P: 0.95
- Top-K: 20
```

---

## 4. Kodingan Repo 1: `CatBubbleCompanion.tsx` (Dengan Skeleton Loading)

Komponen ini menangani loading iframe saat Streamlit sedang *cold-start* atau memuat server:

```tsx
import React, { useState } from 'react';

export const CatBubbleCompanion: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Ganti dengan URL deployment Streamlit kamu di Streamlit Community Cloud
  const STREAMLIT_URL = "https://fathifadhil-bot.streamlit.app/?embed=true";

  const handleOpen = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // Reset loading state setiap dibuka untuk memastikan status iframe terpantau
      setIsLoading(true);
    }
  };

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col items-end font-sans">
      {/* Jendela Pop-up Chat */}
      {isOpen && (
        <div className="w-[350px] sm:w-[400px] h-[540px] bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-2xl shadow-2xl overflow-hidden mb-3 flex flex-col relative animate-in fade-in slide-in-from-bottom-5 duration-200">
          
          {/* Header Bar */}
          <div className="bg-emerald-600 text-white px-4 py-3 flex justify-between items-center z-10 shadow-sm">
            <div className="flex items-center gap-2">
              <span className="text-xl">🐱</span>
              <div>
                <h3 className="text-sm font-semibold leading-tight">Neko Companion</h3>
                <p className="text-[11px] text-emerald-100">Asisten AI Portofolio Fathi</p>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-emerald-100 hover:text-white text-lg font-bold p-1 transition"
              aria-label="Tutup Obrolan"
            >
              ✕
            </button>
          </div>

          {/* SKELETON LOADING (Tampil selama Streamlit iframe memuat) */}
          {isLoading && (
            <div className="absolute inset-0 top-[53px] bg-zinc-50 dark:bg-zinc-950 p-4 flex flex-col justify-between z-20 pointer-events-none">
              <div className="space-y-4">
                {/* Banner Status Loading */}
                <div className="flex items-center gap-2 p-2.5 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-xl text-xs text-emerald-700 dark:text-emerald-300">
                  <span className="animate-spin text-sm">🐾</span>
                  <span>Membangunkan Neko di cloud... Mohon tunggu sebentar!</span>
                </div>

                {/* Skeleton Chat Bubbles */}
                <div className="flex gap-2 items-start">
                  <div className="w-8 h-8 rounded-full bg-zinc-200 dark:bg-zinc-800 animate-pulse shrink-0" />
                  <div className="w-3/4 space-y-2">
                    <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded animate-pulse" />
                    <div className="h-4 w-5/6 bg-zinc-200 dark:bg-zinc-800 rounded animate-pulse" />
                  </div>
                </div>

                <div className="flex justify-end">
                  <div className="w-2/3 h-10 bg-emerald-100 dark:bg-emerald-900/40 rounded-2xl rounded-br-none animate-pulse" />
                </div>

                <div className="flex gap-2 items-start">
                  <div className="w-8 h-8 rounded-full bg-zinc-200 dark:bg-zinc-800 animate-pulse shrink-0" />
                  <div className="w-4/5 space-y-2">
                    <div className="h-4 bg-zinc-200 dark:bg-zinc-800 rounded animate-pulse" />
                    <div className="h-4 w-1/2 bg-zinc-200 dark:bg-zinc-800 rounded animate-pulse" />
                  </div>
                </div>
              </div>

              {/* Skeleton Input Bar */}
              <div className="h-11 w-full bg-zinc-200 dark:bg-zinc-800 rounded-xl animate-pulse" />
            </div>
          )}

          {/* Iframe Streamlit App */}
          <iframe
            src={STREAMLIT_URL}
            onLoad={() => setIsLoading(false)}
            className="w-full flex-1 border-none"
            title="Neko Portfolio Companion"
            allow="clipboard-write"
          />
        </div>
      )}

      {/* Floating Action Button (Maskot Kucing) */}
      <button
        onClick={handleOpen}
        className="group relative flex items-center justify-center w-14 h-14 bg-emerald-600 hover:bg-emerald-700 text-white rounded-full shadow-lg hover:scale-105 transition-all duration-200"
        aria-label="Buka Chat Asisten Portofolio"
      >
        <span className="text-2xl transition-transform group-hover:scale-110">
          {isOpen ? '🐾' : '🐱'}
        </span>
        {!isOpen && (
          <span className="absolute -top-1 -right-1 flex h-3.5 w-3.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3.5 w-3.5 bg-emerald-500"></span>
          </span>
        )}
      </button>
    </div>
  );
};
```

---

## 5. Kodingan Repo 2 (Streamlit AI Service)

### A. File `knowledge/portfolio_data.py` (Knowledge Base)
```python
PORTFOLIO_CONTEXT = """
PROFIL UTAMA:
Nama: Fathi Fadhil
Domain: fathifadhil.me
Fokus Keahlian: Full Stack Web Developer & Flutter Mobile Specialist

TECH STACK:
- Mobile: Flutter, Dart, State Management (Bloc, Provider, Riverpod), SQLite, Offline-First Architecture.
- Frontend & Web: React, Next.js, TypeScript, Tailwind CSS, HTML5/CSS3.
- Backend & Database: Node.js, Python, Express, PostgreSQL, MySQL, Firebase Firestore, REST API.
- DevOps & Tools: Git, GitHub, Docker, Vercel, Postman.

PROYEK UNGGULAN:
1. Mobile E-Commerce / POS Application
   - Tech: Flutter, Firebase, REST API, Bloc State Management.
   - Fitur: Manajemen katalog, keranjang belanja offline-to-online, integrasi cetak struk kasir Bluetooth.
2. Web Platform Portofolio & Interactive AI Showcase
   - Tech: Next.js, Tailwind CSS, Streamlit, Google Gemini API.
   - Fitur: Portofolio modern responsif dengan integrasi asisten virtual Neko.
3. Dashboard Monitoring & Management System
   - Tech: React, Node.js, PostgreSQL.
   - Fitur: Otentikasi JWT, role-based user access, analitik data visual.

KONTAK & KOLABORASI:
- Pengunjung dapat menghubungi melalui form kontak atau tautan sosial media resmi di https://fathifadhil.me.
"""
```

### B. File `app.py` (Streamlit Entrypoint + Gemini + Firebase)
```python
import streamlit as st
from google import genai
from google.genai import types
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
from knowledge.portfolio_data import PORTFOLIO_CONTEXT

# 1. Konfigurasi Halaman & Styling
st.set_page_config(page_title="Neko Assistant", page_icon="🐱", layout="centered")

st.markdown("""
<style>
    /* Hilangkan padding berlebih & header bawaan Streamlit untuk embed */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 2rem; padding-left: 1rem; padding-right: 1rem;}
    .stChatMessage {border-radius: 12px; margin-bottom: 6px;}
</style>
""", unsafe_allow_html=True)

# 2. Inisialisasi Firebase Firestore (Stateful Memory)
if not firebase_admin._apps:
    try:
        firebase_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(firebase_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.warning(f"Firebase offline mode: {e}")

try:
    db = firestore.client()
except Exception:
    db = None

# 3. Inisialisasi Gemini Client
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    st.error("API Key Gemini belum diatur di secrets.")
    st.stop()

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=GEMINI_KEY)

if "session_id" not in st.session_state:
    st.session_state.session_id = f"session_{uuid.uuid4().hex[:8]}"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo meow! 🐾 Aku Neko, asisten Fathi Fadhil. Mau tanya seputar proyek Flutter, Full Stack, atau keahlian Fathi?"}
    ]

# 4. Render Riwayat Chat
for msg in st.session_state.messages:
    avatar = "🐱" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 5. Handle Input User
user_input = st.chat_input("Tanya proyek atau keahlian Fathi...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Simpan ke Firestore
    if db:
        try:
            db.collection("chat_sessions").document(st.session_state.session_id)\
              .collection("messages").add({
                  "role": "user",
                  "text": user_input,
                  "timestamp": firestore.SERVER_TIMESTAMP
              })
        except Exception:
            pass

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
    if db:
        try:
            db.collection("chat_sessions").document(st.session_state.session_id)\
              .collection("messages").add({
                  "role": "assistant",
                  "text": reply,
                  "timestamp": firestore.SERVER_TIMESTAMP
              })
        except Exception:
            pass
```

### C. File `requirements.txt`
```
streamlit>=1.35.0
google-genai>=1.0.0
firebase-admin>=6.5.0
```

### D. File `.streamlit/config.toml`
```toml
[client]
toolbarMode = "minimal"

[theme]
primaryColor = "#059669"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F4F4F5"
textColor = "#18181B"
```

### E. Format Secrets di Streamlit Community Cloud
Di menu **App Settings > Secrets**, masukkan:
```toml
GEMINI_API_KEY = "AIzaSy..."

[firebase]
type = "service_account"
project_id = "fathifadhil-portfolio"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "firebase-adminsdk-...@fathifadhil-portfolio.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
```
