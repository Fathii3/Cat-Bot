import streamlit as st
from components.icons import ICON

def show_skeleton(is_en: bool = True):
    """Animasi loading saat ai memproses jawaban."""
    label = "fetty is thinking" if is_en else "fetty lagi mikir"
    st.markdown(f"""
    <div class="skeleton-box">
        <div class="thinking-pill">
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
    """, unsafe_allow_html=True)

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

def render_top_navbar(active_session: dict, is_en: bool = True):
    """Navbar atas sesi chat aktif."""
    time_label = "Created" if is_en else "Dibuat"
    status_label = "Active" if is_en else "Aktif"
    st.markdown(f"""
    <div class="top-navbar">
        <div class="nav-left">
            <div class="nav-avatar">{ICON["cat"]}</div>
            <div>
                <div class="nav-title">{active_session['title']}</div>
                <div class="nav-time">{ICON["clock"]} {time_label} {active_session['created']}</div>
            </div>
        </div>
        <div class="nav-badge">
            <span class="status-dot"></span> {status_label}
        </div>
    </div>
    """, unsafe_allow_html=True)
