import streamlit as st
from components.icons import ICON

def show_skeleton():
    """Animasi loading saat ai memproses jawaban."""
    st.markdown("""
    <div class="skeleton-box">
        <div class="thinking-pill">
            <span>fetty lagi mikir</span>
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
    """, unsafe_allow_html=True)

def show_callout(text: str, type: str = "tip", title: str = None):
    """Kotak pesan informasi atau peringatan."""
    icon_map = {
        "tip": ICON["lightbulb"],
        "warning": ICON["alert"],
        "info": ICON["info"],
        "check": ICON["check"]
    }
    icon_svg = icon_map.get(type, ICON["info"])
    title_html = f'<div class="callout-title">{title}</div>' if title else ""
    st.markdown(f"""
    <div class="callout callout-{type}">
        <div class="callout-icon">{icon_svg}</div>
        <div class="callout-content">
            {title_html}
            {text}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_brand():
    """Header brand pada sidebar."""
    st.markdown(f"""
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
    """, unsafe_allow_html=True)

def render_top_navbar(active_session: dict):
    """Navbar atas sesi chat aktif."""
    st.markdown(f"""
    <div class="top-navbar">
        <div class="nav-left">
            <div class="nav-avatar">{ICON["cat"]}</div>
            <div>
                <div class="nav-title">{active_session['title']}</div>
                <div class="nav-time">{ICON["clock"]} Dibuat {active_session['created']}</div>
            </div>
        </div>
        <div class="nav-badge">
            <span class="status-dot"></span> Aktif
        </div>
    </div>
    """, unsafe_allow_html=True)
