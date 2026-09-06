import time
import streamlit as st
from google import genai
from google.genai import types

# daftar model gemini
CANDIDATE_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-flash-latest",
]

def load_gemini_keys() -> list[str]:
    """ambil kunci gemini dari secrets."""
    keys = []
    # format list
    raw_keys = st.secrets.get("GEMINI_API_KEYS", [])
    if isinstance(raw_keys, (list, tuple)):
        for k in raw_keys:
            s = str(k).strip()
            if s and s not in keys:
                keys.append(s)
    elif isinstance(raw_keys, str) and raw_keys.strip():
        keys.append(raw_keys.strip())

    # format bernomor 1 sampai 9
    for i in range(1, 10):
        k = st.secrets.get(f"GEMINI_API_KEY_{i}")
        if k and str(k).strip():
            s = str(k).strip()
            if s not in keys:
                keys.append(s)

    # format tunggal
    single = st.secrets.get("GEMINI_API_KEY")
    if single and str(single).strip():
        s = str(single).strip()
        if s not in keys:
            keys.append(s)

    return keys

def init_gemini_state(api_keys: list[str]):
    """inisialisasi client dan rotasi key."""
    if "gemini_clients" not in st.session_state:
        st.session_state.gemini_clients = {}
    if "key_index" not in st.session_state:
        st.session_state.key_index = 0
    if "key_usage" not in st.session_state:
        st.session_state.key_usage = {i: 0 for i in range(len(api_keys))}
    if "key_cooldowns" not in st.session_state:
        st.session_state.key_cooldowns = {}

def get_client_for_key(api_keys: list[str], idx: int) -> genai.Client:
    """ambil atau buat client gemini."""
    if idx not in st.session_state.gemini_clients:
        st.session_state.gemini_clients[idx] = genai.Client(api_key=api_keys[idx])
    return st.session_state.gemini_clients[idx]

def get_next_healthy_key_index(api_keys: list[str]) -> int:
    """pilih key aktif berikutnya dan lewati yang cooldown."""
    now = time.time()
    n = len(api_keys)
    if n <= 1:
        return 0

    # bersihkan cooldown yang selesai
    expired = [k for k, exp in st.session_state.key_cooldowns.items() if now >= exp]
    for k in expired:
        del st.session_state.key_cooldowns[k]

    # cari key yang aktif
    healthy_indices = [i for i in range(n) if i not in st.session_state.key_cooldowns]
    if not healthy_indices:
        # jika semua cooldown, pilih yang tercepat selesai
        return min(st.session_state.key_cooldowns.keys(), key=lambda x: st.session_state.key_cooldowns[x])

    # rotasi key bergantian
    start = st.session_state.key_index
    for offset in range(n):
        candidate = (start + offset) % n
        if candidate in healthy_indices:
            st.session_state.key_index = (candidate + 1) % n
            return candidate

    return healthy_indices[0]

def mark_key_cooldown(key_idx: int, duration_seconds: int = 60):
    """beri jeda untuk key yang terkena limit."""
    st.session_state.key_cooldowns[key_idx] = time.time() + duration_seconds

# peta badge teknologi
TECH_BADGE_MAP = {
    "next.js": "![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white)",
    "react": "![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)",
    "typescript": "![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)",
    "tailwind css": "![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)",
    "tailwind": "![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white)",
    "framer motion": "![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?logo=framer&logoColor=white)",
    "node.js": "![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs&logoColor=white)",
    "flutter": "![Flutter](https://img.shields.io/badge/Flutter-02569B?logo=flutter&logoColor=white)",
    "dart": "![Dart](https://img.shields.io/badge/Dart-0175C2?logo=dart&logoColor=white)",
    "python": "![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)",
    "sqlite": "![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)",
    "sqflite": "![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)",
    "gemini ai": "![Gemini AI](https://img.shields.io/badge/Gemini_AI-8E75FF?logo=google&logoColor=white)",
    "google gemini ai": "![Gemini AI](https://img.shields.io/badge/Gemini_AI-8E75FF?logo=google&logoColor=white)",
    "google gemini ai api": "![Gemini AI](https://img.shields.io/badge/Gemini_AI-8E75FF?logo=google&logoColor=white)",
    "firebase": "![Firebase](https://img.shields.io/badge/Firebase-FFCA28?logo=firebase&logoColor=black)",
    "supabase": "![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?logo=supabase&logoColor=white)",
    "postgresql": "![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)",
    "mysql": "![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)",
    "laravel": "![Laravel](https://img.shields.io/badge/Laravel-FF2D20?logo=laravel&logoColor=white)",
    "laravel 13": "![Laravel](https://img.shields.io/badge/Laravel-FF2D20?logo=laravel&logoColor=white)",
    "php": "![PHP](https://img.shields.io/badge/PHP-777BB4?logo=php&logoColor=white)",
    "php 8.3": "![PHP](https://img.shields.io/badge/PHP-777BB4?logo=php&logoColor=white)",
    "docker": "![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)",
    "git": "![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)",
    "github": "![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)",
    "vite": "![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)",
    "express.js": "![Express.js](https://img.shields.io/badge/Express.js-000000?logo=express&logoColor=white)",
    "javascript": "![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)",
    "html5": "![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)",
    "css3": "![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)",
    "streamlit": "![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)",
    "google gemini": "![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?logo=google&logoColor=white)",
    "gemini api": "![Gemini API](https://img.shields.io/badge/Gemini_API-8E75FF?logo=google&logoColor=white)",
    "lucide icons": "![Lucide Icons](https://img.shields.io/badge/Lucide_Icons-F56565?logo=lucide&logoColor=white)",
}

def format_tech_badges(text: str) -> str:
    """ubah teks daftar teknologi menjadi badge visual jika belum ada gambar."""
    if not text:
        return text
    lines = text.split("\n")
    formatted_lines = []
    for line in lines:
        lower_line = line.lower()
        if ("tech:" in lower_line or "tech stack:" in lower_line or "teknologi:" in lower_line) and "![" not in line:
            prefix, _, tech_part = line.partition(":")
            items = [t.strip() for t in tech_part.split(",") if t.strip()]
            badges = []
            for item in items:
                clean_item = item.strip("`*-_ \t")
                key = clean_item.lower()
                if key in TECH_BADGE_MAP:
                    badges.append(TECH_BADGE_MAP[key])
                else:
                    badges.append(f"`{clean_item}`")
            if badges:
                formatted_lines.append(f"{prefix}: {' '.join(badges)}")
                continue
        formatted_lines.append(line)
    return "\n".join(formatted_lines)

def build_system_instruction(portfolio_context: str) -> str:
    """instruksi sistem untuk persona fetty."""
    return f"""Kamu adalah "fetty", asisten virtual pintar sekaligus maskot kucing interaktif resmi untuk Fathi Fadhil di fathifadhil.me.

Peran & Tugas:
1. Membantu pengunjung, klien, dan recruiter mengenal keahlian Fathi Fadhil sebagai Full Stack & Flutter Developer.
2. Membedah arsitektur, tantangan teknis, dan solusi dari proyek-proyek yang telah dikerjakan Fathi.
3. Menyarankan proyek atau tech stack yang relevan sesuai kebutuhan pertanyaan pengunjung.
4. Memberikan informasi kontak resmi Fathi jika pengunjung ingin berkolaborasi atau menawarkan pekerjaan.

Karakter & Persona:
- Ramah, sopan, antusias, namun tetap teknikal dan berwibawa.
- Gunakan sentuhan persona kucing yang ramah dan menggemaskan secara halus (misal menyapa dengan "meow!"), namun tetap profesional di mata recruiter.
- Berbahasa Indonesia santai-profesional secara default, namun WAJIB otomatis membalas dalam Bahasa Inggris jika pengunjung bertanya dalam Bahasa Inggris.

Tampilan Tech Stack & Badges:
- Setiap kali menyebutkan teknologi, tech stack, atau alat pada proyek atau keahlian Fathi, SELALU tampilkan deretan badge visual Shields.io (misalnya: ![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white) ![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white) ![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?logo=framer&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs&logoColor=white)).
- Khusus untuk proyek Dist (dist.nex.biz.id), tampilkan status dan badgenya:
  ![Production](https://img.shields.io/badge/Production-dist.nex.biz.id-00df8f?logo=vercel&logoColor=white&labelColor=222222) ![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white) ![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white) ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?logo=tailwindcss&logoColor=white) ![Framer Motion](https://img.shields.io/badge/Framer_Motion-0055FF?logo=framer&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-339933?logo=nodedotjs&logoColor=white)

Batasan:
- HANYA jawab pertanyaan seputar Fathi Fadhil, portofolio, proyek, tech stack, sertifikasi, pengalaman, dan kolaborasi teknis.
- Jika ada pertanyaan di luar topik, tolak secara halus: "Maaf meow, Fetty hanya bisa menjawab seputar portofolio dan keahlian Fathi! Ada proyek atau tech stack yang ingin kamu diskusikan?"
- Jangan pernah mengarang proyek, sertifikasi, atau fakta yang tidak ada di Knowledge Base.
- Jawab maksimal 3-5 kalimat singkat padat kecuali diminta detail.

Knowledge Base:
{portfolio_context}
"""

def generate_fetty_response(
    api_keys: list[str],
    messages: list[dict],
    user_input: str,
    portfolio_context: str
) -> tuple[str | None, Exception | None]:
    """kirim chat ke gemini dengan rotasi key dan model cadangan."""
    system_instruction = build_system_instruction(portfolio_context)
    chat_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=0.2,
        top_p=0.95,
        top_k=20
    )

    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages[-6:]])
    prompt = f"Riwayat percakapan:\n{history_text}\n\nPertanyaan user:\n{user_input}"

    reply = None
    last_error = None
    keys_count = max(1, len(api_keys))
    max_key_attempts = min(keys_count, 5)

    # kirim pesan dengan rotasi key
    for attempt in range(max_key_attempts):
        key_idx = get_next_healthy_key_index(api_keys)
        client = get_client_for_key(api_keys, key_idx)
        success = False

        for model_name in CANDIDATE_MODELS:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=chat_config
                )
                if response and response.text:
                    reply = response.text
                    st.session_state.key_usage[key_idx] = st.session_state.key_usage.get(key_idx, 0) + 1
                    success = True
                    break
            except Exception as e:
                last_error = e
                err_str = str(e)
                # jika limit, beri jeda dan ganti key
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "API_KEY_INVALID" in err_str or "quota" in err_str.lower():
                    mark_key_cooldown(key_idx, duration_seconds=60)
                    break
                continue

        if success:
            break

    if reply:
        reply = format_tech_badges(reply)

    return reply, last_error
