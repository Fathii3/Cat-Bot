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
