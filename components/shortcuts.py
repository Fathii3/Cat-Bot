import streamlit as st

# daftar pintasan topik ke pertanyaan portofolio
QUICK_TOPICS = {
    "📁 Projek": "Boleh ceritakan apa saja proyek-proyek unggulan yang pernah dikerjakan oleh Fathi?",
    "📜 Sertifikat": "Apa saja sertifikasi profesional dan lisensi yang dimiliki oleh Fathi?",
    "💼 Pengalaman": "Bagaimana riwayat pengalaman kerja dan perjalanan profesional Fathi?",
    "⚡ Tech": "Teknologi dan tech stack apa saja yang dikuasai oleh Fathi?",
    "🐙 GitHub": "Bagaimana aktivitas GitHub dan repositori open-source milik Fathi?",
    "🌐 Sosial Media": "Di mana saja tautan media sosial dan kontak resmi Fathi Fadhil untuk terhubung?",
}

def on_pill_change():
    """Aksi saat pintasan topik diklik."""
    chosen = st.session_state.get("quick_pill_selection")
    if chosen:
        st.session_state["pending_pill_prompt"] = QUICK_TOPICS.get(chosen, chosen)
        st.session_state["quick_pill_selection"] = None  # reset agar tidak terkunci

def render_quick_pills():
    """Tampilkan pintasan topik dengan st.pills."""
    st.caption("💡 Pintasan Cepat:")
    st.pills(
        label="Pintasan Topik",
        options=list(QUICK_TOPICS.keys()),
        selection_mode="single",
        label_visibility="collapsed",
        key="quick_pill_selection",
        on_change=on_pill_change
    )
