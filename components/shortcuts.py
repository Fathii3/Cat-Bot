import streamlit as st

# daftar pintasan topik ke pertanyaan portofolio
QUICK_TOPICS_ID = {
    "📁 Projek Unggulan": "Boleh ceritakan apa saja proyek-proyek unggulan yang pernah dikerjakan oleh Fathi?",
    "⚡ Tech Stack": "Teknologi dan tech stack apa saja yang dikuasai oleh Fathi?",
    "🚀 Alur Kerja": "Bagaimana workflow dan metodologi Fathi dari ide hingga menjadi produk?",
    "📜 Sertifikasi": "Apa saja sertifikasi profesional dan lisensi yang dimiliki oleh Fathi?",
    "💼 Pengalaman": "Bagaimana riwayat pengalaman kerja dan perjalanan profesional Fathi?",
    "🌐 Kontak": "Di mana saja tautan media sosial dan kontak resmi Fathi Fadhil untuk terhubung?",
}

QUICK_TOPICS_EN = {
    "📁 Featured Projects": "What are Fathi's most notable engineering projects and what problems did they solve?",
    "⚡ Tech Stack": "What core tech stack and tools does Fathi specialize in?",
    "🚀 Workflow": "How does Fathi take an idea from concept to a production-ready product?",
    "📜 Certifications": "What professional certifications and licenses does Fathi hold?",
    "💼 Experience": "Can you summarize Fathi's work experience and engineering journey?",
    "🌐 Connect": "Where can I find Fathi Fadhil's official social media and contact links?",
}

QUICK_TOPICS = QUICK_TOPICS_EN

def on_pill_change():
    """Aksi saat pintasan topik diklik."""
    chosen = st.session_state.get("quick_pill_selection")
    if chosen:
        prompt = QUICK_TOPICS_EN.get(chosen) or QUICK_TOPICS_ID.get(chosen) or chosen
        st.session_state["pending_pill_prompt"] = prompt
        st.session_state["quick_pill_selection"] = None  # reset agar tidak terkunci

def render_quick_pills(is_en: bool = True):
    """Tampilkan pintasan topik dengan st.pills."""
    topics = QUICK_TOPICS_EN if is_en else QUICK_TOPICS_ID
    st.caption("💡 Quick Prompts:" if is_en else "💡 Pintasan Cepat:")
    st.pills(
        label="Pintasan Topik",
        options=list(topics.keys()),
        selection_mode="single",
        label_visibility="collapsed",
        key="quick_pill_selection",
        on_change=on_pill_change
    )

HERO_PROMPT_CARDS_EN = [
    {
        "icon": "📁",
        "title": "Featured Projects",
        "desc": "Key production apps & full-stack systems",
        "prompt": QUICK_TOPICS_EN["📁 Featured Projects"],
    },
    {
        "icon": "⚡",
        "title": "Tech Stack & Skills",
        "desc": "Flutter, Next.js, Python, TypeScript & Cloud",
        "prompt": QUICK_TOPICS_EN["⚡ Tech Stack"],
    },
    {
        "icon": "🚀",
        "title": "Dev Workflow",
        "desc": "From concept to production-ready product",
        "prompt": QUICK_TOPICS_EN["🚀 Workflow"],
    },
    {
        "icon": "📜",
        "title": "Certifications",
        "desc": "Professional licenses & verified credentials",
        "prompt": QUICK_TOPICS_EN["📜 Certifications"],
    },
    {
        "icon": "💼",
        "title": "Work Experience",
        "desc": "Engineering journey & professional background",
        "prompt": QUICK_TOPICS_EN["💼 Experience"],
    },
    {
        "icon": "🌐",
        "title": "Connect & Links",
        "desc": "Official social links & collaboration",
        "prompt": QUICK_TOPICS_EN["🌐 Connect"],
    },
]

HERO_PROMPT_CARDS_ID = [
    {
        "icon": "📁",
        "title": "Projek Unggulan",
        "desc": "Sistem produksi & aplikasi full-stack",
        "prompt": QUICK_TOPICS_ID["📁 Projek Unggulan"],
    },
    {
        "icon": "⚡",
        "title": "Tech Stack & Keahlian",
        "desc": "Flutter, Next.js, Python, TypeScript & Cloud",
        "prompt": QUICK_TOPICS_ID["⚡ Tech Stack"],
    },
    {
        "icon": "🚀",
        "title": "Alur Kerja Dev",
        "desc": "Dari rancangan arsitektur hingga rilis",
        "prompt": QUICK_TOPICS_ID["🚀 Alur Kerja"],
    },
    {
        "icon": "📜",
        "title": "Sertifikasi & Lisensi",
        "desc": "Lisensi profesional & kredensial terverifikasi",
        "prompt": QUICK_TOPICS_ID["📜 Sertifikasi"],
    },
    {
        "icon": "💼",
        "title": "Pengalaman Kerja",
        "desc": "Riwayat karir & pencapaian profesional",
        "prompt": QUICK_TOPICS_ID["💼 Pengalaman"],
    },
    {
        "icon": "🌐",
        "title": "Kontak & Jejaring",
        "desc": "Tautan media sosial & tawaran kolaborasi",
        "prompt": QUICK_TOPICS_ID["🌐 Kontak"],
    },
]

def render_hero_prompt_cards(is_en: bool = True):
    """Tampilkan kartu saran topik ala Google Gemini di bawah welcome hero."""
    cards = HERO_PROMPT_CARDS_EN if is_en else HERO_PROMPT_CARDS_ID

    st.markdown('<div class="hero-prompt-grid">', unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, card in enumerate(cards):
        col = cols[idx % 2]
        with col:
            btn_label = f"{card['icon']}  **{card['title']}**\n\n{card['desc']}"
            if st.button(
                btn_label,
                key=f"hero_card_{idx}",
                use_container_width=True,
                help=card["prompt"],
            ):
                st.session_state["pending_pill_prompt"] = card["prompt"]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)



