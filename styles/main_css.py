import streamlit as st

def apply_custom_css():
    """Gaya tampilan aplikasi."""
    st.markdown("""
<style>
    /* header & tombol sidebar */
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stToolbarActions"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: auto !important;
        z-index: 99 !important;
        padding: 4px 8px !important;
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

    /* tata letak konten */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* animasi */
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

    /* pesan chat & avatar */
    .stChatMessage {
        border-radius: 14px;
        margin-bottom: 8px;
        animation: fadeInUp 0.3s cubic-bezier(0.22, 1, 0.36, 1);
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

    /* baris sesi */
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 6px !important;
        margin-bottom: 3px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:first-child,
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child,
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child {
        flex: 0 0 38px !important;
        min-width: 38px !important;
        max-width: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* tombol hapus sesi */
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child button,
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child button,
    section[data-testid="stSidebar"] button[key*="del_"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 36px !important;
        height: 36px !important;
        min-height: 36px !important;
        max-height: 36px !important;
        padding: 0 !important;
        margin: 0 !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child button:hover,
    section[data-testid="stSidebar"] button[key*="del_"]:hover {
        background: #fef2f2 !important;
        border-color: #fecaca !important;
        color: #ef4444 !important;
        transform: scale(1.06) !important;
        box-shadow: 0 2px 6px rgba(239, 68, 68, 0.15) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child button:active,
    section[data-testid="stSidebar"] button[key*="del_"]:active {
        transform: scale(0.96) !important;
        background: #fee2e2 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child button span,
    section[data-testid="stSidebar"] button[key*="del_"] span {
        color: inherit !important;
    }
    section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child button:hover span,
    section[data-testid="stSidebar"] button[key*="del_"]:hover span {
        color: #ef4444 !important;
    }

    /* tampilan mobile */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
        }
        section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child {
            flex: 0 0 38px !important;
            min-width: 38px !important;
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
        animation: fadeInUp 0.3s ease;
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

    /* kotak info */
    .callout {
        border-radius: 12px;
        padding: 12px 14px;
        margin: 8px 0;
        font-size: 13px;
        line-height: 1.5;
        display: flex;
        align-items: flex-start;
        gap: 10px;
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
        animation: fadeInUp 0.3s ease;
    }
    .callout-icon {
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
        border-radius: 7px;
    }
    .callout-content {
        flex: 1;
        min-width: 0 !important;
        overflow-wrap: break-word !important;
        word-break: break-word !important;
    }
    .callout code {
        word-break: break-all !important;
        white-space: pre-wrap !important;
        max-width: 100% !important;
        font-size: 11.5px !important;
        border-radius: 6px !important;
        padding: 4px 6px !important;
    }
    .callout-title {
        font-weight: 600;
        margin-bottom: 2px;
        font-size: 13px;
    }
    .callout-tip {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #166534;
    }
    .callout-tip .callout-icon { background: #dcfce7; color: #16a34a; }
    .callout-warning {
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #92400e;
    }
    .callout-warning .callout-icon { background: #fef3c7; color: #d97706; }
    .callout-info {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        color: #075985;
    }
    .callout-info .callout-icon { background: #e0f2fe; color: #0284c7; }

    /* kolom input chat */
    [data-testid="stChatInput"] {
        border-radius: 16px !important;
        border: 1.5px solid #e5e7eb !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
        transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1) !important;
        background: #ffffff !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #059669 !important;
        box-shadow: 0 4px 24px rgba(5, 150, 105, 0.16) !important;
    }
    [data-testid="stChatInput"] textarea {
        font-size: 14px !important;
        line-height: 1.5 !important;
    }
    [data-testid="stChatInput"] button {
        border-radius: 10px !important;
        color: #059669 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stChatInput"] button:hover {
        background: #ecfdf5 !important;
        transform: scale(1.08) !important;
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
