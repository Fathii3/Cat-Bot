import streamlit as st

def apply_custom_css():
    """Gaya tampilan aplikasi."""
    st.markdown("""
<style>
    /*
     * Layout seperti ChatGPT/Gemini/Claude:
     * - Seluruh halaman scroll (block-container)
     * - Chat input fixed melayang di bawah viewport
     * - Padding-bottom di chat area supaya konten tidak ketutup input
     */
    html, body, #root, .withScreencast, .stApp {
        height: 100% !important;
        margin: 0 !important;
        overflow: hidden !important;
    }

    .stAppViewContainer {
        height: 100dvh !important;
        height: 100vh !important;
        overflow: hidden !important;
    }

    section[data-testid="stMain"],
    section.main, .stMain {
        height: 100% !important;
        overflow-y: auto !important;
        overflow-x: hidden !important;
    }

    /* biarkan Streamlit internal container flow natural */
    [data-testid="stAppScrollToBottomContainer"] {
        overflow: visible !important;
    }

    /* area chat — scroll natural, padding bawah cukup supaya tidak ketutup chat input */
    .block-container {
        overflow: visible !important;
        padding-top: 1rem !important;
        padding-bottom: 100px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* chat input FIXED melayang di bawah viewport — seperti Gemini/ChatGPT */
    [data-testid="stBottom"] {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: linear-gradient(to bottom, rgba(255,255,255,0) 0%, #ffffff 15%, #ffffff 100%) !important;
        border-top: none !important;
        box-shadow: none !important;
        padding: 16px 14px 12px 14px !important;
        z-index: 100 !important;
    }

    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"] {
        max-width: 100% !important;
    }

    #MainMenu { display: none !important; }
    footer { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stToolbarActions"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }

    /* sentuhan responsif tombol & elemen interaktif (tanpa delay 300ms) */
    button, input, textarea, a, select,
    [data-testid="stChatInput"],
    [data-testid="stChatInputSubmitButton"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"],
    [data-testid="stDownloadButton"] button,
    [data-testid="stButtonGroup"] button,
    [data-testid="stPills"] button {
        touch-action: manipulation !important;
        pointer-events: auto !important;
        -webkit-tap-highlight-color: transparent !important;
    }

    /* pastikan sidebar tetap dapat disentuh dan di-scroll */
    section[data-testid="stSidebar"] {
        pointer-events: auto !important;
        z-index: 1000 !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: auto !important;
        z-index: 99 !important;
        padding: 4px 8px !important;
        pointer-events: none !important;
    }
    header[data-testid="stHeader"] * {
        pointer-events: auto !important;
    }

    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: inline-flex !important;
        background: #ffffff !important;
        border: 1.5px solid #059669 !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.2) !important;
        color: #059669 !important;
        padding: 6px 10px !important;
        margin: 6px 8px !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
    }
    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover {
        background: #ecfdf5 !important;
        transform: scale(1.06) translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3) !important;
    }
    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: #059669 !important;
        stroke: #059669 !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: inline-flex !important;
    }
    [data-testid="stSidebarCollapseButton"] button {
        border-radius: 8px !important;
        color: #71717a !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover {
        background: #f0fdf4 !important;
        color: #059669 !important;
    }

    /* animasi */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes skeleton-shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    @keyframes dotPulse {
        0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
        40% { transform: scale(1); opacity: 1; }
    }

    /* pesan chat & avatar — opacity-only fade, tanpa transform yang bikin layout shift */
    .stChatMessage {
        border-radius: 14px;
        margin-bottom: 8px;
        animation: fadeIn 0.25s ease;
    }
    .stChatMessage [data-testid="stChatMessageAvatarCustom"],
    .stChatMessage [data-testid="stChatMessageAvatarImage"] {
        border-radius: 10px !important;
        box-shadow: 0 2px 6px rgba(5, 150, 105, 0.18) !important;
    }
    .stChatMessage p img {
        border-radius: 4px !important;
        box-shadow: none !important;
        margin: 2px 3px 2px 0 !important;
        vertical-align: middle !important;
        display: inline-block !important;
    }

    /* sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fafbfc 0%, #f4f7f5 100%);
        border-right: 1px solid #e5e7eb;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem;
    }

    /* brand header */
    .sidebar-brand {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        padding: 4px 2px 14px 2px !important;
        margin-bottom: 12px !important;
        border-bottom: 1px solid #f1f5f9 !important;
    }
    .sidebar-brand .brand-icon {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 38px !important;
        height: 38px !important;
        border-radius: 11px !important;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        flex-shrink: 0 !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.22) !important;
    }
    .sidebar-brand .brand-icon svg {
        width: 21px !important;
        height: 21px !important;
        stroke: #ffffff !important;
        stroke-width: 2.2 !important;
        fill: none !important;
    }
    .sidebar-brand .brand-text {
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        gap: 3px !important;
        min-width: 0 !important;
    }
    .sidebar-brand .brand-title {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        letter-spacing: -0.2px !important;
        line-height: 1.2 !important;
    }
    .sidebar-brand .brand-status {
        display: inline-flex !important;
        align-items: center !important;
        gap: 5px !important;
        margin: 0 !important;
        padding: 0 !important;
        font-size: 11.5px !important;
        color: #64748b !important;
        line-height: 1.2 !important;
        font-weight: 500 !important;
    }
    .sidebar-brand .status-dot {
        width: 6px !important;
        height: 6px !important;
        border-radius: 50% !important;
        background: #10b981 !important;
        flex-shrink: 0 !important;
        display: inline-block !important;
    }

    /* toggle switch bahasa (clean segmented pill) */
    section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] {
        margin: 2px 0 10px 0 !important;
        width: 100% !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] > div {
        width: 100% !important;
        background: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 3px !important;
        display: flex !important;
        gap: 4px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button {
        flex: 1 !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 12.5px !important;
        border: none !important;
        padding: 6px 12px !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
        color: #64748b !important;
        background: transparent !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button:hover {
        color: #0f172a !important;
        background: rgba(255, 255, 255, 0.7) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button[aria-checked="true"],
    section[data-testid="stSidebar"] [data-testid="stSegmentedControl"] button[data-checked="true"] {
        background: #ffffff !important;
        color: #059669 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
    }

    .sidebar-section-title {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #94a3b8;
        padding: 12px 4px 6px 4px;
    }

    .sidebar-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 4px 4px 4px;
        font-size: 11.5px;
        color: #94a3b8;
    }

    /* tombol chat baru */
    section[data-testid="stSidebar"] button[kind="primary"] {
        border-radius: 11px !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        padding: 10px 16px !important;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        border: none !important;
        color: white !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.2) !important;
    }
    section[data-testid="stSidebar"] button[kind="primary"]:hover {
        transform: translateY(-1.5px) !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35) !important;
    }
    section[data-testid="stSidebar"] button[kind="primary"]:active {
        transform: translateY(0) scale(0.98) !important;
    }

    /* daftar sesi */
    section[data-testid="stSidebar"] button[kind="secondary"] {
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        text-align: left !important;
        padding: 9px 12px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: #334155 !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
        line-height: 1.3 !important;
    }
    section[data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #0f172a !important;
        transform: translateX(2px) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
    }

    /* sesi aktif */
    section[data-testid="stSidebar"] button[kind="secondary"]:disabled {
        border-color: #a7f3d0 !important;
        background: #ecfdf5 !important;
        color: #065f46 !important;
        font-weight: 600 !important;
        opacity: 1 !important;
        box-shadow: 0 1px 3px rgba(5, 150, 105, 0.1) !important;
    }

    /* baris sesi chat di sidebar */
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 6px !important;
        margin-bottom: 4px !important;
        width: 100% !important;
    }

    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
        flex: 0 0 38px !important;
        width: 38px !important;
        min-width: 38px !important;
    }

    /* tombol popover opsi sesi */
    section[data-testid="stSidebar"] [data-testid="stPopover"] button {
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 9px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        color: #64748b !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stPopover"] button:hover {
        border-color: #059669 !important;
        color: #059669 !important;
        background: #f0fdf4 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stPopover"] button p {
        display: none !important;
    }

    /* tampilan mobile */
    @media (max-width: 768px) {
        /* wadah konten utama selalu 100% penuh di mobile, tidak pernah terhimpit */
        .stAppViewContainer,
        .stAppViewContainer > div:last-child,
        section[data-testid="stMain"],
        section.main,
        .stMain {
            width: 100% !important;
            min-width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 100% !important;
            left: 0 !important;
        }

        /* sidebar di mobile menjadi laci overlay (drawer) melayang di atas chat */
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            bottom: 0 !important;
            height: 100% !important;
            max-height: 100% !important;
            width: 84vw !important;
            max-width: 320px !important;
            min-width: 260px !important;
            z-index: 999999 !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.25) !important;
            transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1) !important;
        }

        /* saat sidebar ditutup di mobile, sembunyikan di luar viewport */
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-110%) !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }

        /* saat sidebar dibuka di mobile, tampil melayang penuh */
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }

        /* navbar atas di mobile */
        .top-navbar {
            padding: 8px 12px !important;
            gap: 8px !important;
        }
        .top-navbar .nav-left {
            gap: 8px !important;
            min-width: 0 !important;
            flex: 1 1 auto !important;
        }
        .top-navbar .nav-title {
            font-size: 13px !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
            max-width: 160px !important;
        }
        .top-navbar .nav-badge {
            padding: 3px 8px !important;
            font-size: 10.5px !important;
            flex-shrink: 0 !important;
        }

        /* baris sesi di mobile */
        section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            gap: 4px !important;
            width: 100% !important;
        }
        section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
            flex: 1 1 auto !important;
            min-width: 0 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
            flex: 0 0 34px !important;
            width: 34px !important;
            min-width: 34px !important;
        }
        section[data-testid="stSidebar"] [data-testid="stPopover"] button {
            width: 34px !important;
            height: 34px !important;
            min-width: 34px !important;
            min-height: 34px !important;
        }

        /* penyesuaian wadah chat input di mobile — tetap fixed melayang */
        [data-testid="stBottom"] {
            padding-left: 8px !important;
            padding-right: 8px !important;
            padding-bottom: env(safe-area-inset-bottom, 8px) !important;
            padding-top: 12px !important;
        }
        [data-testid="stChatInput"] {
            padding: 3px 5px 3px 12px !important;
        }

        /* penyesuaian tombol kirim chat di mobile */
        [data-testid="stChatInput"] button,
        [data-testid="stChatInputSubmitButton"],
        [data-testid="stChatInputStopButton"] {
            width: 34px !important;
            height: 34px !important;
            min-width: 34px !important;
            min-height: 34px !important;
            max-width: 34px !important;
            max-height: 34px !important;
            flex-shrink: 0 !important;
        }
        [data-testid="stChatInput"] button svg,
        [data-testid="stChatInputSubmitButton"] svg {
            width: 18px !important;
            height: 18px !important;
            min-width: 18px !important;
            min-height: 18px !important;
        }
    }

    /* pembatas & keterangan */
    section[data-testid="stSidebar"] hr {
        margin: 8px 0 !important;
        border-color: #f0f0f0 !important;
    }
    section[data-testid="stSidebar"] .stCaption {
        font-size: 11px !important;
        color: #a1a1aa !important;
        padding-left: 4px !important;
    }

    /* navbar atas */
    .top-navbar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        animation: fadeIn 0.3s ease;
    }
    .top-navbar .nav-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .top-navbar .nav-avatar {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 6px rgba(5, 150, 105, 0.2);
        flex-shrink: 0;
    }
    .top-navbar .nav-title {
        font-size: 13.5px;
        font-weight: 600;
        color: #0f172a;
        line-height: 1.2;
    }
    .top-navbar .nav-time {
        font-size: 11px;
        color: #64748b;
        margin-top: 2px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .top-navbar .nav-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 9px;
        background: #ecfdf5;
        border: 1px solid #d1fae5;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        color: #065f46;
    }
    .top-navbar .nav-badge .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #10b981;
        display: inline-block;
        box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25);
    }

    /* efek loading */
    .skeleton-box {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 4px 0 8px 0;
        width: 100%;
        max-width: 520px;
        animation: fadeInUp 0.25s ease;
    }
    .thinking-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 500;
        color: #059669;
        background: #ecfdf5;
        border: 1px solid #d1fae5;
        border-radius: 14px;
        padding: 4px 11px;
        width: fit-content;
    }
    .pulse-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #059669;
        animation: dotPulse 1.2s ease-in-out infinite;
    }
    .pulse-dot:nth-child(2) { animation-delay: 0.2s; }
    .pulse-dot:nth-child(3) { animation-delay: 0.4s; }

    .skeleton-bars {
        display: flex;
        flex-direction: column;
        gap: 8px;
        width: 100%;
    }
    .skeleton-bar {
        height: 10px;
        border-radius: 6px;
        background: linear-gradient(90deg, #f0fdf4 25%, #d1fae5 50%, #f0fdf4 75%);
        background-size: 200% 100%;
        animation: skeleton-shimmer 1.4s ease-in-out infinite;
    }
    .skeleton-bar.w-full { width: 92%; }
    .skeleton-bar.w-3-4 { width: 72%; }
    .skeleton-bar.w-1-2 { width: 42%; }

    /* kolom input chat */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 1.5px solid #e2e8f0 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1) !important;
        background: #ffffff !important;
        padding: 4px 6px 4px 14px !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #059669 !important;
        box-shadow: 0 4px 24px rgba(5, 150, 105, 0.16) !important;
    }
    [data-testid="stChatInput"] textarea {
        font-size: 14px !important;
        line-height: 1.5 !important;
        color: #1e293b !important;
    }

    /* sembunyikan instruksi internal atau elemen artefak visual */
    [data-testid="stChatInput"] .stChatInputInstructions {
        display: none !important;
    }

    /* tombol kirim pesan chat input (stChatInputSubmitButton) */
    [data-testid="stChatInput"] button,
    [data-testid="stChatInputSubmitButton"],
    [data-testid="stChatInputStopButton"] {
        width: 36px !important;
        height: 36px !important;
        min-width: 36px !important;
        min-height: 36px !important;
        max-width: 36px !important;
        max-height: 36px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        margin: 0 !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: none !important;
        outline: none !important;
        cursor: pointer !important;
        touch-action: manipulation !important;
        pointer-events: auto !important;
        -webkit-tap-highlight-color: transparent !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
        box-sizing: border-box !important;
        position: relative !important;
    }

    /* hilangkan artefak pseudo-element & outline fokus liar */
    [data-testid="stChatInput"] button::before,
    [data-testid="stChatInput"] button::after,
    [data-testid="stChatInputSubmitButton"]::before,
    [data-testid="stChatInputSubmitButton"]::after {
        display: none !important;
        content: none !important;
    }
    [data-testid="stChatInput"] button:focus,
    [data-testid="stChatInput"] button:focus-visible,
    [data-testid="stChatInputSubmitButton"]:focus,
    [data-testid="stChatInputSubmitButton"]:focus-visible {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(5, 150, 105, 0.25) !important;
    }

    /* tombol kirim saat aktif (siap kirim pesan) */
    [data-testid="stChatInput"] button:not(:disabled),
    [data-testid="stChatInputSubmitButton"]:not(:disabled) {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(5, 150, 105, 0.35) !important;
        cursor: pointer !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInput"] button:not(:disabled):hover,
    [data-testid="stChatInputSubmitButton"]:not(:disabled):hover {
        background: linear-gradient(135deg, #047857 0%, #059669 100%) !important;
        transform: scale(1.08) !important;
        box-shadow: 0 4px 14px rgba(5, 150, 105, 0.45) !important;
    }
    [data-testid="stChatInput"] button:not(:disabled):active,
    [data-testid="stChatInputSubmitButton"]:not(:disabled):active {
        transform: scale(0.95) !important;
        background: #065f46 !important;
    }

    /* tombol kirim saat dinonaktifkan (belum ketik / kuota habis) */
    [data-testid="stChatInput"] button:disabled,
    [data-testid="stChatInputSubmitButton"]:disabled {
        background: #f1f5f9 !important;
        color: #94a3b8 !important;
        border: 1px solid #e2e8f0 !important;
        cursor: not-allowed !important;
        opacity: 0.85 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* tombol stop respon ai jika muncul */
    [data-testid="stChatInputStopButton"] {
        background: #fee2e2 !important;
        color: #ef4444 !important;
        border: 1px solid #fecaca !important;
    }
    [data-testid="stChatInputStopButton"]:hover {
        background: #fecaca !important;
        color: #dc2626 !important;
        transform: scale(1.08) !important;
    }

    /* ikon svg di dalam tombol kirim pesan */
    [data-testid="stChatInput"] button span,
    [data-testid="stChatInputSubmitButton"] span {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: inherit !important;
    }
    [data-testid="stChatInput"] button svg,
    [data-testid="stChatInputSubmitButton"] svg {
        width: 20px !important;
        height: 20px !important;
        min-width: 20px !important;
        min-height: 20px !important;
        display: block !important;
        margin: auto !important;
        color: inherit !important;
        fill: currentColor !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stChatInput"] button svg path[fill="none"],
    [data-testid="stChatInputSubmitButton"] svg path[fill="none"] {
        fill: none !important;
    }
    [data-testid="stChatInput"] button svg path:not([fill="none"]),
    [data-testid="stChatInputSubmitButton"] svg path:not([fill="none"]) {
        fill: currentColor !important;
    }
    [data-testid="stChatInput"] button [data-testid="stIconMaterial"],
    [data-testid="stChatInputSubmitButton"] [data-testid="stIconMaterial"] {
        color: inherit !important;
        font-size: 20px !important;
    }

    /* tombol aksi */
    [data-testid="stBaseButton-secondary"] {
        border-radius: 10px !important;
        font-size: 12px !important;
        padding: 4px 12px !important;
        border: 1px solid #e5e7eb !important;
        color: #6b7280 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stBaseButton-secondary"]:hover {
        border-color: #059669 !important;
        color: #059669 !important;
        background: #f0fdf4 !important;
    }

    /* tombol bersihkan chat */
    button[key="clear_chat"] {
        border-radius: 8px !important;
        font-size: 11.5px !important;
        padding: 3px 10px !important;
        color: #9ca3af !important;
        border: 1px solid #f3f4f6 !important;
        background: transparent !important;
        transition: all 0.2s ease !important;
    }
    button[key="clear_chat"]:hover {
        color: #ef4444 !important;
        border-color: #fecaca !important;
        background: #fef2f2 !important;
    }

    /* tombol topik st.pills */
    [data-testid="stButtonGroup"] button,
    [data-testid="stPills"] button {
        border-radius: 18px !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        padding: 5px 12px !important;
        border: 1px solid #e2e8f0 !important;
        background: #ffffff !important;
        color: #334155 !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    }
    [data-testid="stButtonGroup"] button:hover,
    [data-testid="stPills"] button:hover {
        border-color: #059669 !important;
        background: #f0fdf4 !important;
        color: #059669 !important;
        transform: translateY(-1.5px) !important;
        box-shadow: 0 3px 8px rgba(5, 150, 105, 0.15) !important;
    }
    [data-testid="stButtonGroup"] button[aria-pressed="true"],
    [data-testid="stPills"] button[aria-pressed="true"] {
        background: #059669 !important;
        border-color: #059669 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)
