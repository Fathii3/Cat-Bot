import textwrap
import streamlit as st
from .icons import ICON

def show_skeleton(is_en: bool = True):
    """Animasi loading saat AI memproses jawaban."""
    label = "Fetty is thinking..." if is_en else "Fetty lagi mikir..."
    html = textwrap.dedent(f"""
    <div class="skeleton-box">
        <div class="thinking-pill">
            <span class="thinking-cat">{ICON["cat"]}</span>
            <span>{label}</span>
            <span class="pulse-dot"></span>
            <span class="pulse-dot"></span>
            <span class="pulse-dot"></span>
        </div>
        <div class="skeleton-bars">
            <div class="skeleton-bar w-full"></div>
            <div class="skeleton-bar w-3-4"></div>
            <div class="skeleton-bar w-1-2"></div>
        </div>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)

def render_welcome_hero(is_en: bool = True):
    """Tampilan hero sambutan selamat datang ala Google Gemini."""
    greeting = "How can Fetty help with Fathi's work today?" if is_en else "Ada yang ingin kamu tanyakan seputar Fathi Fadhil?"
    subtext = (
        "Interactive AI companion for Fathi Fadhil's engineering portfolio. Ask about featured projects, full-stack tech stack, dev workflow, or work experience!"
        if is_en
        else "Asisten AI resmi portofolio Fathi Fadhil. Cari tahu seputar proyek unggulan, tech stack, alur pengembangan sistem, hingga pengalaman kerja!"
    )
    html = textwrap.dedent(f"""
    <div class="welcome-hero">
        <div class="hero-avatar-wrap">
            <div class="hero-avatar-glow"></div>
            <div class="hero-avatar">{ICON["cat"]}</div>
        </div>
        <h2 class="hero-title">{greeting}</h2>
        <p class="hero-subtitle">{subtext}</p>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)

def show_callout(text: str, type: str = "tip", title: str = None):
    """Kotak pesan informasi atau peringatan menggunakan API bawaan Streamlit."""
    msg = f"**{title}**\n\n{text}" if title else text
    if type == "warning":
        st.warning(msg, icon=":material/warning:")
    elif type == "check":
        st.success(msg, icon=":material/check_circle:")
    else:
        st.info(msg, icon=":material/lightbulb:")

def render_sidebar_brand():
    """Header brand pada sidebar."""
    html = textwrap.dedent(f"""
    <div class="sidebar-brand">
        <div class="brand-icon">{ICON["cat"]}</div>
        <div class="brand-text">
            <div class="brand-title">Fetty Assistant</div>
            <div class="brand-status">
                <span class="status-dot"></span>
                <span>Online · Portfolio AI</span>
            </div>
        </div>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)

def render_top_navbar(active_session: dict = None, is_en: bool = True, limit_info: dict = None):
    """Navbar atas sesi chat aktif dengan tampilan clean modern tanpa badge model."""
    time_label = "Created" if is_en else "Dibuat"
    status_label = "Online" if is_en else "Online"
    session_data = active_session or {}
    title = session_data.get("title", "New Chat" if is_en else "Chat Baru")
    created = session_data.get("created", "")

    quota_badge = ""
    if limit_info:
        rem = limit_info.get("remaining_questions", 5)
        lim = limit_info.get("limit", 5)
        cd = limit_info.get("cooldown_remaining", 0)
        if cd > 0:
            quota_badge = f'<span class="nav-quota-pill cd">⏳ {cd}s</span>'
        else:
            quota_badge = f'<span class="nav-quota-pill">🐾 {rem}/{lim}</span>'

    created_meta = f'<span class="meta-dot">·</span><span>{time_label} {created}</span>' if created else ""

    html = textwrap.dedent(f"""
    <div class="top-navbar">
        <div class="nav-left">
            <div class="nav-avatar">{ICON["cat"]}</div>
            <div class="nav-info">
                <div class="nav-title-row">
                    <span class="nav-title" title="{title}">{title}</span>
                    {quota_badge}
                </div>
                <div class="nav-meta">
                    <span class="status-dot"></span>
                    <span>{status_label}</span>
                    {created_meta}
                </div>
            </div>
        </div>
    </div>
    """).strip()
    st.markdown(html, unsafe_allow_html=True)
