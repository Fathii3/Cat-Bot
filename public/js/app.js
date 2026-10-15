// Sanitasi HTML
function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// State global
let isEn = false;
try {
  const initParams = new URLSearchParams(window.location.search);
  const qLang = initParams.get('lang');
  if (qLang) {
    isEn = qLang.toLowerCase().startsWith('en');
  } else {
    const saved = localStorage.getItem('fetty_lang');
    if (saved) {
      isEn = saved.toLowerCase().startsWith('en');
    }
  }
} catch (_) {}
let sessions = {};
let activeSessionId = null;
let isGenerating = false;
let remainingQuota = 5;
let quotaResetAt = null;

// Data direktori topik & prompt unggulan
const HERO_CARDS = {
  en: [
    {
      tag: "FEATURED SYSTEMS",
      icon: "ri-code-box-line",
      title: "Production Projects",
      desc: "FINARA (Offline-First POS & Gemini AI), SKM Langkat (Public Survey), Dist & SiBanjir.",
      prompt: "What are Fathi's most notable engineering projects and what architectures did they use?"
    },
    {
      tag: "CORE ARCHITECTURE",
      icon: "ri-stack-line",
      title: "Tech Stack & Mastery",
      desc: "Flutter, Dart, Next.js 14, TypeScript, Laravel 13, Firebase, Supabase, Google Gemini API.",
      prompt: "What technical stack, languages, and frameworks does Fathi specialize in?"
    },
    {
      tag: "METHODOLOGY",
      icon: "ri-git-branch-line",
      title: "Idea to Product Workflow",
      desc: "Discovery (Needs) → Strategy (Architecture) → Build (Code) → Testing → Zero-Downtime Release.",
      prompt: "How does Fathi's engineering workflow translate an idea into a production-ready product?"
    },
    {
      tag: "CREDENTIALS",
      icon: "ri-award-line",
      title: "Certifications & Experience",
      desc: "Google Developer Groups #JuaraVibeCoding, Huawei HCIA-AI, IBM SkillsBuild, Diskominfo PKL.",
      prompt: "What professional certifications, licenses, and industry experience does Fathi possess?"
    }
  ],
  id: [
    {
      tag: "SISTEM PRODUKSI",
      icon: "ri-code-box-line",
      title: "Proyek & Aplikasi Unggulan",
      desc: "FINARA (Offline-First POS & Gemini AI), SKM Langkat (Survei IKM Diskominfo), Dist & SiBanjir.",
      prompt: "Boleh ceritakan arsitektur dan solusi teknis pada proyek-proyek unggulan Fathi Fadhil?"
    },
    {
      tag: "ARSITEKTUR & STACK",
      icon: "ri-stack-line",
      title: "Tech Stack & Spesialisasi",
      desc: "Flutter, Dart, Next.js 14, TypeScript, Laravel 13, Firebase, Supabase, Google Gemini API.",
      prompt: "Teknologi, bahasa pemrograman, dan framework apa saja yang dikuasai oleh Fathi Fadhil?"
    },
    {
      tag: "METODOLOGI DEV",
      icon: "ri-git-branch-line",
      title: "Alur Kerja: Dari Ide ke Rilis",
      desc: "Discovery (Kebutuhan) → Strategy (Arsitektur) → Build (Coding) → Testing → Rilis Produksi.",
      prompt: "Bagaimana alur kerja Fathi dari merancang ide hingga menjadi produk siap rilis?"
    },
    {
      tag: "KREDENSIAL & RIWAYAT",
      icon: "ri-award-line",
      title: "Sertifikasi & Pengalaman",
      desc: "Google Developer Groups #JuaraVibeCoding, Huawei HCIA-AI, IBM SkillsBuild, PKL Diskominfo.",
      prompt: "Apa saja sertifikasi profesional, lisensi, dan pengalaman kerja yang dimiliki oleh Fathi Fadhil?"
    }
  ]
};

const QUICK_PILLS = {
  en: [
    { label: "FINARA POS (Flutter)", prompt: "Explain the FINARA app, its offline-first architecture, and Gemini AI integration." },
    { label: "SKM Langkat (Laravel 13)", prompt: "Tell me about the SKM Langkat public survey platform and its security features." },
    { label: "Full-Stack Tech Stack", prompt: "What core frontend, backend, and mobile technologies does Fathi master?" },
    { label: "Workflow: Idea to Release", prompt: "How does Fathi manage the development lifecycle from discovery to release?" },
    { label: "Certifications & Awards", prompt: "What certifications from Google, Huawei, and IBM does Fathi hold?" },
    { label: "Contact & Collaboration", prompt: "How can I contact Fathi for freelance or full-time opportunities?" }
  ],
  id: [
    { label: "FINARA POS (Flutter)", prompt: "Jelaskan tentang aplikasi FINARA, arsitektur offline-first, dan integrasi Gemini AI-nya." },
    { label: "SKM Langkat (Laravel 13)", prompt: "Ceritakan tentang platform survei publik SKM Langkat dan proteksi keamanannya." },
    { label: "Tech Stack & Spesialisasi", prompt: "Apa saja teknologi frontend, backend, dan mobile yang dikuasai Fathi?" },
    { label: "Workflow Ide ke Rilis", prompt: "Bagaimana alur kerja Fathi dari memahami kebutuhan hingga peluncuran sistem?" },
    { label: "Sertifikasi GDG & Huawei", prompt: "Apa saja sertifikasi resmi dari Google, Huawei, dan IBM yang dimiliki Fathi?" },
    { label: "Kontak & Kolaborasi", prompt: "Bagaimana cara menghubungi Fathi untuk peluang kerja sama atau proyek freelance?" }
  ]
};

// Pengelolaan kuota bergulir 12 jam (WIB / GMT+7)
function formatWibTime(timestamp) {
  if (!timestamp) return '12 jam lagi';
  try {
    const formatter = new Intl.DateTimeFormat('id-ID', {
      timeZone: 'Asia/Jakarta',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false
    });
    return `${formatter.format(new Date(timestamp)).replace('.', ':')} WIB`;
  } catch (e) {
    const d = new Date(timestamp);
    const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
    const wib = new Date(utc + (3600000 * 7));
    const h = String(wib.getHours()).padStart(2, '0');
    const m = String(wib.getMinutes()).padStart(2, '0');
    return `${h}:${m} WIB`;
  }
}

function getNextResetTimeWib() {
  if (!quotaResetAt) {
    // Estimasi 12 jam dari waktu sekarang jika belum mulai dipakai
    return formatWibTime(Date.now() + (12 * 60 * 60 * 1000));
  }
  return formatWibTime(quotaResetAt);
}

function checkAndResetQuota() {
  const now = Date.now();
  try {
    const quotaRecord = JSON.parse(localStorage.getItem('fetty_quota') || '{}');
    if (quotaRecord.resetAt && now >= quotaRecord.resetAt) {
      // Waktu 12 jam sejak limit tercapai telah usai! Reset kembali ke 5
      remainingQuota = 5;
      quotaResetAt = null;
      localStorage.setItem('fetty_quota', JSON.stringify({ remaining: 5, resetAt: null }));
    } else if (quotaRecord.resetAt && now < quotaRecord.resetAt) {
      // Masih dalam masa cooldown 12 jam setelah limit tercapai
      remainingQuota = 0;
      quotaResetAt = quotaRecord.resetAt;
    } else {
      // Belum mencapai limit
      remainingQuota = typeof quotaRecord.remaining === 'number' ? Math.max(0, quotaRecord.remaining) : 5;
      if (remainingQuota === 0) {
        quotaResetAt = now + (12 * 60 * 60 * 1000);
        localStorage.setItem('fetty_quota', JSON.stringify({ remaining: 0, resetAt: quotaResetAt }));
      } else {
        quotaResetAt = null;
      }
    }
  } catch (e) {
    console.warn("Storage quota error:", e);
    remainingQuota = 5;
    quotaResetAt = null;
  }
}

// Inisialisasi aplikasi
function initApp() {
  // Kuota 12 jam bergulir (WIB)
  checkAndResetQuota();

  // Riwayat chat lokal
  try {
    const savedSessions = JSON.parse(localStorage.getItem('fetty_sessions') || '{}');
    const savedActiveId = localStorage.getItem('fetty_active_session_id');
    if (savedSessions && Object.keys(savedSessions).length > 0) {
      sessions = savedSessions;
      if (savedActiveId && sessions[savedActiveId]) {
        activeSessionId = savedActiveId;
      } else {
        activeSessionId = Object.keys(sessions)[0];
      }
    } else {
      createNewChat(false);
    }
  } catch (e) {
    console.warn("Storage sessions error:", e);
    createNewChat(false);
  }

  // Inisialisasi bahasa: 1. URL param (?lang=en/id), 2. localStorage, 3. sesi aktif, 4. default false (ID)
  try {
    const params = new URLSearchParams(window.location.search);
    const urlLang = params.get('lang');
    if (urlLang) {
      isEn = urlLang.toLowerCase().startsWith('en');
      localStorage.setItem('fetty_lang', isEn ? 'en' : 'id');
    } else {
      const savedLang = localStorage.getItem('fetty_lang');
      if (savedLang) {
        isEn = savedLang.toLowerCase().startsWith('en');
      } else if (activeSessionId && sessions[activeSessionId]?.lang) {
        isEn = sessions[activeSessionId].lang === 'en';
      }
    }
  } catch (e) {
    console.warn("Language init error:", e);
  }

  // Sinkronisasi bahasa lintas frame / iframe embed (misal dari portfolio fathifadhil.me)
  window.addEventListener('message', (event) => {
    try {
      if (event.data) {
        const raw = event.data.lang || (event.data.type === 'SET_LANGUAGE' ? event.data.value : null);
        if (typeof raw === 'string') {
          const toEn = raw.toLowerCase().startsWith('en');
          if (toEn !== isEn) {
            setLanguage(toEn);
          }
        }
      }
    } catch (_) {}
  });

  updateLanguageUI();
  renderSessionsList();
  renderActiveSession();
  updateQuotaUI();
  initSlideDeleteEvents();
  initSpeechRecognition();

  const inputBox = document.querySelector('.chat-input-box');
  if (inputBox) {
    inputBox.addEventListener('click', () => {
      if (remainingQuota <= 0) {
        showQuotaExceededModal();
      }
    });
  }

  // Toggle sidebar
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const toggleBtn = document.getElementById('btn-toggle-sidebar');

  window.closeMobileSidebar = function () {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
  };

  window.openMobileSidebar = function () {
    sidebar.classList.add('open');
    overlay.classList.add('active');
  };

  toggleBtn.addEventListener('click', () => {
    if (window.innerWidth <= 768) {
      if (sidebar.classList.contains('open')) {
        window.closeMobileSidebar();
      } else {
        window.openMobileSidebar();
      }
    } else {
      sidebar.classList.toggle('collapsed');
    }
  });

  overlay.addEventListener('click', window.closeMobileSidebar);

  window.addEventListener('resize', () => {
    updateLanguageUI();
    if (window.innerWidth > 768) {
      overlay.classList.remove('active');
      sidebar.classList.remove('open');
    }
  });
}

// Notifikasi toast
function showToast(msg, duration = 2800) {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = 'toast-msg';
  toast.innerHTML = `<i class="ri-information-line"></i><span>${escapeHtml(msg)}</span>`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    toast.style.transition = 'all 0.25s ease';
    setTimeout(() => toast.remove(), 250);
  }, duration);
}

// Modal popup modern pengganti alert
function openAppModal({
  icon = 'ri-flashlight-line',
  iconType = 'default',
  badge = 'NOTIFIKASI',
  title = 'Informasi',
  desc = '',
  showCallout = true,
  calloutHeader = 'Ingin diskusi proyek atau freelance langsung?',
  calloutDesc = 'Hubungi Fathi langsung via WhatsApp resmi atau telusuri portofolio lengkapnya.',
  confirmText = 'Mengerti',
  onConfirm = null
}) {
  const modal = document.getElementById('app-modal');
  if (!modal) return;

  const iconBox = document.getElementById('modal-icon-box');
  if (iconBox) {
    iconBox.className = 'app-modal-icon-wrapper ' + (iconType !== 'default' ? iconType : '');
  }
  const iconEl = document.getElementById('modal-icon');
  if (iconEl) iconEl.className = icon;

  const badgeEl = document.getElementById('modal-badge');
  if (badgeEl) badgeEl.textContent = badge;

  const titleEl = document.getElementById('modal-title');
  if (titleEl) titleEl.textContent = title;

  const descEl = document.getElementById('modal-desc');
  if (descEl) descEl.textContent = desc;

  const calloutEl = document.getElementById('modal-callout');
  if (calloutEl) {
    calloutEl.style.display = showCallout ? 'block' : 'none';
    const ch = calloutEl.querySelector('.callout-header span');
    if (ch) ch.textContent = calloutHeader;
    const cd = calloutEl.querySelector('p');
    if (cd) cd.textContent = calloutDesc;
  }

  const btnConfirm = document.getElementById('modal-btn-confirm');
  if (btnConfirm) {
    btnConfirm.textContent = confirmText;
    btnConfirm.onclick = () => {
      closeAppModal();
      if (typeof onConfirm === 'function') onConfirm();
    };
  }

  modal.style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function closeAppModal(e) {
  if (e && e.target && e.target !== e.currentTarget && !e.target.closest('.app-modal-close') && !e.target.closest('#modal-btn-confirm')) {
    return;
  }
  const modal = document.getElementById('app-modal');
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

function showQuotaExceededModal() {
  const nextReset = getNextResetTimeWib();
  openAppModal({
    icon: 'ri-flashlight-line',
    iconType: 'warning',
    badge: isEn ? 'QUOTA LIMIT REACHED' : 'BATAS LIMIT TERCAPAI',
    title: isEn ? 'Limit Reached (5 Questions)' : 'Batas 5 Pertanyaan Tercapai',
    desc: isEn
      ? `You have reached the 5-question limit. Your quota will reset 12 hours from now at ${nextReset}.`
      : `Kamu telah mencapai batas limit 5 pertanyaan. Kuota kamu akan direset 12 jam dari sekarang pada pukul ${nextReset}.`,
    showCallout: true,
    calloutHeader: isEn ? 'Need direct collaboration or freelance project?' : 'Ingin diskusi proyek atau freelance langsung?',
    calloutDesc: isEn
      ? 'Reach out to Fathi directly via WhatsApp or browse his complete portfolio.'
      : 'Hubungi Fathi langsung via WhatsApp resmi atau telusuri portofolio lengkapnya.',
    confirmText: isEn ? 'Got it' : 'Mengerti'
  });
}

// Kuota & bahasa
function updateQuotaUI() {
  checkAndResetQuota();
  const qText = `${remainingQuota}/5`;
  const badge = document.getElementById('nav-quota-badge');
  if (badge) {
    const label = isEn ? 'Quota: ' : 'Sisa Kuota: ';
    badge.innerHTML = `<i class="ri-flashlight-line"></i> <span id="nav-quota-val"><span class="quota-label">${label}</span><span class="quota-val">${qText}</span></span>`;
    if (quotaResetAt) {
      const nextReset = getNextResetTimeWib();
      badge.title = isEn
        ? `Limit reached (Resets at ${nextReset})`
        : `Batas limit tercapai (Reset pukul ${nextReset})`;
    } else {
      badge.title = isEn
        ? "5 questions quota (12-hour cooldown starts once limit is reached)"
        : "Kuota 5 pertanyaan (Reset 12 jam dihitung saat limit tercapai)";
    }
  }
  const totalSess = Object.keys(sessions).length;
  const sidebarQuota = document.getElementById('sidebar-quota-text');
  if (sidebarQuota) {
    sidebarQuota.textContent = isEn
      ? `${totalSess} chats saved • Quota: ${qText}`
      : `${totalSess} obrolan tersimpan • Kuota: ${qText}`;
    if (quotaResetAt) {
      const nextReset = getNextResetTimeWib();
      sidebarQuota.title = isEn ? `Resets at ${nextReset}` : `Reset pukul ${nextReset}`;
    } else {
      sidebarQuota.title = isEn
        ? "12-hour cooldown starts after limit"
        : "Reset 12 jam dihitung setelah limit";
    }
  }

  const input = document.getElementById('chat-input');
  if (remainingQuota <= 0) {
    const nextReset = getNextResetTimeWib();
    input.disabled = true;
    input.placeholder = isEn
      ? `Limit reached (5/5). Resets at ${nextReset}`
      : `Batas kuota habis (5/5). Reset pukul ${nextReset}`;
  } else {
    input.disabled = false;
  }
}

function recordQuestionUsage() {
  checkAndResetQuota();
  remainingQuota = Math.max(0, remainingQuota - 1);
  const now = Date.now();
  // Timer 12 jam baru mulai dihitung saat kuota benar-benar habis (limit tercapai)!
  if (remainingQuota === 0) {
    if (!quotaResetAt || now >= quotaResetAt) {
      quotaResetAt = now + (12 * 60 * 60 * 1000); // 12 jam dari saat limit tercapai!
    }
  } else {
    quotaResetAt = null;
  }
  try {
    localStorage.setItem('fetty_quota', JSON.stringify({
      remaining: remainingQuota,
      resetAt: quotaResetAt
    }));
  } catch (e) { }
  updateQuotaUI();
}

function setLanguage(toEn, savePref = true) {
  isEn = !!toEn;
  if (savePref) {
    try {
      localStorage.setItem('fetty_lang', isEn ? 'en' : 'id');
    } catch (_) { }
  }
  if (activeSessionId && sessions[activeSessionId]) {
    sessions[activeSessionId].lang = isEn ? 'en' : 'id';
    saveSessions();
  }
  updateLanguageUI();
  renderHeroCards();
  renderQuickPills();
  updateQuotaUI();
  resetSlideState();
}

function updateLanguageUI() {
  document.querySelectorAll('.lang-btn-en').forEach(el => el.classList.toggle('active', isEn));
  document.querySelectorAll('.lang-btn-id').forEach(el => el.classList.toggle('active', !isEn));
  const elEn = document.getElementById('lang-en');
  if (elEn) elEn.classList.toggle('active', isEn);
  const elId = document.getElementById('lang-id');
  if (elId) elId.classList.toggle('active', !isEn);
  document.getElementById('txt-new-chat').textContent = isEn ? "New Chat" : "Obrolan Baru";
  document.getElementById('txt-history-title').textContent = isEn ? "Conversation Archive" : "Arsip Percakapan";
  const brandStatus = document.getElementById('txt-brand-status');
  if (brandStatus) {
    brandStatus.textContent = "Online";
  }
  document.getElementById('hero-title').textContent = isEn
    ? "Explore Fathi Fadhil's Engineering Portfolio"
    : "Eksplorasi Rekayasa & Portofolio Fathi Fadhil";
  document.getElementById('hero-subtitle').textContent = isEn
    ? "Official technical AI companion. Analyze production architectures (FINARA, SKM Langkat, Dist), Flutter mobile solutions, full-stack systems, and end-to-end release workflows."
    : "Asisten interaktif resmi seputar arsitektur sistem (FINARA, SKM Langkat, Dist), implementasi mobile Flutter, tech stack modern, dan alur rilis produksi.";
  document.getElementById('txt-thinking-label').textContent = isEn ? "Analyzing portfolio knowledge base..." : "Menganalisis basis pengetahuan portofolio...";

  const txtBtnDl = document.getElementById('txt-btn-download');
  if (txtBtnDl) txtBtnDl.textContent = isEn ? "Download Chat" : "Unduh Obrolan";
  const btnDl = document.getElementById('btn-download-chat');
  if (btnDl) btnDl.title = isEn ? "Download this chat (.txt)" : "Unduh obrolan ini (.txt)";

  const txtBtnDel = document.getElementById('txt-btn-delete');
  if (txtBtnDel) txtBtnDel.textContent = isEn ? "Delete Chat" : "Hapus Obrolan";
  const btnDel = document.getElementById('btn-trigger-delete');
  if (btnDel) btnDel.title = isEn ? "Delete this chat" : "Hapus obrolan ini";

  const quotaBadge = document.getElementById('nav-quota-badge');
  if (quotaBadge) {
    const nextReset = getNextResetTimeWib();
    quotaBadge.title = isEn
      ? `Chat quota (Resets every 12h · Next reset: ${nextReset})`
      : `Sisa kuota obrolan (Reset setiap 12 jam · Reset berikutnya: ${nextReset})`;
  }

  const txtSlide = document.getElementById('txt-slide-label');
  if (txtSlide) txtSlide.textContent = isEn ? "Swipe right to delete chat" : "Geser ke kanan untuk hapus chat";

  const footerCaption = document.getElementById('chat-footer-caption');
  if (footerCaption) {
    footerCaption.innerHTML = isEn
      ? `Powered by Google Gemini · Inquiring into projects & experience of <a href="https://fathifadhil.me" target="_blank">Fathi Fadhil ↗</a>`
      : `Didukung Google Gemini · Menjawab seputar proyek & pengalaman <a href="https://fathifadhil.me" target="_blank">Fathi Fadhil ↗</a>`;
  }

  const input = document.getElementById('chat-input');
  if (remainingQuota > 0 && !isListeningSpeech) {
    if (window.innerWidth <= 640) {
      input.placeholder = isEn ? "Ask about Fathi's projects..." : "Tanya seputar proyek Fathi...";
    } else {
      input.placeholder = isEn ? "Ask about FINARA, tech stack, or release workflow..." : "Tanyakan studi kasus FINARA, tech stack, atau alur rilis...";
    }
  }

  renderHeroCards();
  renderQuickPills();
}

// Render hero & kartu direktori
function renderHeroCards() {
  const container = document.getElementById('hero-cards-container');
  if (!container) return;
  container.innerHTML = '';
  const cards = isEn ? HERO_CARDS.en : HERO_CARDS.id;
  cards.forEach(c => {
    const div = document.createElement('div');
    div.className = 'hero-card';
    div.innerHTML = `
      <div class="hero-card-header">
        <span class="hero-card-tag">${escapeHtml(c.tag)}</span>
        <div class="hero-card-icon flex-center">
          <i class="${escapeHtml(c.icon)}"></i>
        </div>
      </div>
      <div class="hero-card-title">${escapeHtml(c.title)}</div>
      <div class="hero-card-desc">${escapeHtml(c.desc)}</div>
      <div class="hero-card-cta">
        <span>${isEn ? 'Explore topic' : 'Mulai tanya'}</span>
        <i class="ri-arrow-right-up-line"></i>
      </div>
    `;
    div.onclick = () => sendUserMessage(c.prompt);
    container.appendChild(div);
  });
}

function renderQuickPills() {
  const container = document.getElementById('quick-pills-container');
  if (!container) return;
  container.innerHTML = '';
  const pills = isEn ? QUICK_PILLS.en : QUICK_PILLS.id;
  pills.forEach(p => {
    const btn = document.createElement('button');
    btn.className = 'quick-pill';
    btn.type = 'button';
    btn.innerHTML = `<i class="ri-sparkling-line"></i> <span>${escapeHtml(p.label)}</span>`;
    btn.onclick = () => sendUserMessage(p.prompt);
    container.appendChild(btn);
  });
}

// Kelola sesi chat
function createNewChat(switchNow = true) {
  if (typeof window.closeMobileSidebar === 'function') {
    window.closeMobileSidebar();
  }
  const id = 'sess_' + Date.now();
  const defaultTitle = isEn ? "New Chat" : "Obrolan Baru";
  sessions[id] = {
    id,
    title: defaultTitle,
    lang: isEn ? 'en' : 'id',
    created: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    messages: []
  };
  if (switchNow) {
    activeSessionId = id;
  }
  saveSessions();
  if (switchNow) {
    renderSessionsList();
    renderActiveSession();
  }
}

function saveSessions() {
  try {
    localStorage.setItem('fetty_sessions', JSON.stringify(sessions));
    if (activeSessionId) {
      localStorage.setItem('fetty_active_session_id', activeSessionId);
    }
  } catch (e) {
    console.warn("Storage save error:", e);
  }
}

function renderSessionsList() {
  const skeleton = document.getElementById('sessions-skeleton');
  if (skeleton) skeleton.style.display = 'none';
  const list = document.getElementById('sessions-list');
  list.innerHTML = '';
  const sids = Object.keys(sessions).reverse();

  sids.forEach(sid => {
    const sess = sessions[sid];
    const isActive = sid === activeSessionId;
    const item = document.createElement('div');
    item.className = `session-item ${isActive ? 'active' : ''}`;
    const escapedTitle = escapeHtml(sess.title);
    item.innerHTML = `
      <span class="session-item-title" title="${escapedTitle}">${escapedTitle}</span>
      <div class="session-actions">
        <button class="session-action-btn dl flex-center" title="${isEn ? 'Download chat' : 'Unduh obrolan'}" onclick="downloadSessionTxt(event, '${sid}')">
          <i class="ri-download-2-line"></i>
        </button>
        <button class="session-action-btn del flex-center" title="${isEn ? 'Delete chat' : 'Hapus obrolan'}" onclick="deleteSession(event, '${sid}')">
          <i class="ri-delete-bin-line"></i>
        </button>
      </div>
    `;
    item.onclick = (e) => {
      if (!e.target.closest('.session-actions')) {
        activeSessionId = sid;
        saveSessions();
        if (sessions[sid]?.lang) {
          const sessIsEn = sessions[sid].lang === 'en';
          if (sessIsEn !== isEn) {
            setLanguage(sessIsEn, true);
          }
        }
        if (typeof window.closeMobileSidebar === 'function') {
          window.closeMobileSidebar();
        }
        renderSessionsList();
        renderActiveSession();
      }
    };
    list.appendChild(item);
  });
  updateQuotaUI();
}

function deleteSession(e, sid) {
  if (e) e.stopPropagation();
  const targetTitle = sessions[sid] ? sessions[sid].title : '';
  delete sessions[sid];
  if (Object.keys(sessions).length === 0) {
    createNewChat(true);
  } else if (activeSessionId === sid) {
    activeSessionId = Object.keys(sessions)[0];
  }
  saveSessions();
  renderSessionsList();
  renderActiveSession();
  showToast(isEn ? `Deleted: "${targetTitle}"` : `Chat dihapus: "${targetTitle}"`);
}

function renderActiveSession() {
  const sess = sessions[activeSessionId];
  if (!sess) return;
  document.getElementById('nav-session-title').textContent = sess.title;

  const welcomeHero = document.getElementById('welcome-hero');
  const messagesList = document.getElementById('messages-list');
  messagesList.innerHTML = '';

  if (sess.messages.length === 0) {
    welcomeHero.style.display = 'block';
  } else {
    welcomeHero.style.display = 'none';
    sess.messages.forEach(m => appendMessageToDOM(m.role, m.content, m.time));
  }
  scrollToBottom();
}

function appendMessageToDOM(role, content, timeStr) {
  const messagesList = document.getElementById('messages-list');
  const row = document.createElement('div');
  row.className = `message-row ${role}`;

  const avatarSrc = role === 'user' ? '/assets/user_avatar.svg' : '/assets/fetty_avatar.svg';
  const parsed = role === 'assistant' ? marked.parse(content || '') : content.replace(/&/g, '&amp;').replace(/</g, '&lt;');

  if (role === 'assistant') {
    row.innerHTML = `
      <img src="${avatarSrc}" class="message-avatar" alt="Fetty" />
      <div class="message-bubble">
        <div class="bot-md">${parsed}</div>
        <div class="message-time">${timeStr}</div>
      </div>
    `;
  } else {
    row.innerHTML = `
      <div class="message-bubble">
        <div style="white-space: pre-wrap; word-break: break-word;">${parsed}</div>
        <div class="message-time">${timeStr}</div>
      </div>
      <img src="${avatarSrc}" class="message-avatar" alt="User" />
    `;
  }
  messagesList.appendChild(row);
  scrollToBottom();
}

function scrollToBottom() {
  const container = document.getElementById('chat-scroll-container');
  container.scrollTop = container.scrollHeight;
}

// Unduh riwayat .txt
function downloadActiveSessionTxt() {
  downloadSessionTxt(null, activeSessionId);
}

function downloadSessionTxt(e, sid) {
  if (e) e.stopPropagation();
  const targetId = sid || activeSessionId;
  const sess = sessions[targetId];
  if (!sess) return;
  if (!sess.messages || sess.messages.length === 0) {
    showToast(isEn ? "No messages in this chat yet!" : "Belum ada percakapan di sesi ini!");
    return;
  }

  const border = "=".repeat(62);
  const subBorder = "-".repeat(62);
  const nowStr = new Date().toLocaleString(isEn ? 'en-US' : 'id-ID', {
    dateStyle: 'full',
    timeStyle: 'medium'
  });

  let content = `${border}\n`;
  content += `FETTY ASSISTANT · RIWAYAT PERCAKAPAN PORTFOLIO\n`;
  content += `Judul Sesi   : ${sess.title}\n`;
  content += `Waktu Sesi   : ${sess.created || '-'}\n`;
  content += `Diunduh Pada : ${nowStr}\n`;
  content += `Website      : https://fathifadhil.me\n`;
  content += `${border}\n\n`;

  sess.messages.forEach((m, idx) => {
    const roleLabel = m.role === 'user' ? '👤 PENGGUNA' : '🐱 FETTY ASSISTANT';
    content += `[${m.time || ''}] ${roleLabel}:\n`;
    content += `${m.content.trim()}\n\n`;
    if (idx < sess.messages.length - 1) {
      content += `${subBorder}\n\n`;
    }
  });

  content += `${border}\n`;
  content += `Akhir riwayat percakapan. Jelajahi portofolio lengkap di https://fathifadhil.me\n`;
  content += `${border}\n`;

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const cleanTitle = (sess.title || 'chat')
    .toLowerCase()
    .replace(/[^a-z0-9]/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 30) || 'chat';
  const dateStr = new Date().toISOString().slice(0, 10);
  link.href = url;
  link.download = `fetty-chat-${cleanTitle}-${dateStr}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);

  showToast(isEn ? "Chat conversation downloaded (.txt)" : "Riwayat percakapan berhasil diunduh (.txt)");
}

// Geser hapus chat di navbar
let isDraggingSlide = false;
let slideStartX = 0;
let currentSlideX = 0;
let maxSlideDistance = 0;

function toggleSlideDelete(show) {
  const bar = document.getElementById('slide-delete-bar');
  const defBar = document.getElementById('nav-default-bar');
  if (!bar || !defBar) return;
  if (show) {
    bar.classList.add('active');
    defBar.style.display = 'none';
    resetSlideState();
  } else {
    bar.classList.remove('active');
    defBar.style.display = 'flex';
    resetSlideState();
  }
}

function resetSlideState() {
  const thumb = document.getElementById('slide-thumb');
  const fill = document.getElementById('slide-fill');
  const trackText = document.getElementById('slide-track-text');
  if (!thumb || !fill) return;
  thumb.style.transition = 'transform 0.22s ease';
  thumb.style.transform = 'translateX(0px)';
  fill.style.transition = 'width 0.22s ease';
  fill.style.width = '0px';
  currentSlideX = 0;
  isDraggingSlide = false;
  if (trackText) {
    trackText.style.opacity = '1';
    trackText.innerHTML = `<span id="txt-slide-label">${isEn ? 'Swipe right to delete chat' : 'Geser ke kanan untuk hapus chat'}</span> <i class="ri-arrow-right-double-line slide-arrow-anim"></i>`;
  }
}

function initSlideDeleteEvents() {
  const track = document.getElementById('slide-delete-track');
  const thumb = document.getElementById('slide-thumb');
  const fill = document.getElementById('slide-fill');
  const trackText = document.getElementById('slide-track-text');
  if (!track || !thumb) return;

  function startDrag(clientX) {
    isDraggingSlide = true;
    slideStartX = clientX;
    thumb.style.transition = 'none';
    fill.style.transition = 'none';
    maxSlideDistance = Math.max(10, track.clientWidth - thumb.clientWidth - 6);
  }

  function moveDrag(clientX) {
    if (!isDraggingSlide) return;
    const deltaX = clientX - slideStartX;
    currentSlideX = Math.max(0, Math.min(deltaX, maxSlideDistance));
    thumb.style.transform = `translateX(${currentSlideX}px)`;
    fill.style.width = `${currentSlideX + 16}px`;

    const ratio = maxSlideDistance > 0 ? (currentSlideX / maxSlideDistance) : 0;
    if (trackText) {
      trackText.style.opacity = Math.max(0, 1 - ratio * 1.6);
    }
  }

  function endDrag() {
    if (!isDraggingSlide) return;
    isDraggingSlide = false;
    const ratio = maxSlideDistance > 0 ? (currentSlideX / maxSlideDistance) : 0;

    if (ratio >= 0.72) {
      // Geser selesai: hapus
      thumb.style.transition = 'transform 0.15s ease';
      thumb.style.transform = `translateX(${maxSlideDistance}px)`;
      fill.style.transition = 'width 0.15s ease';
      fill.style.width = '100%';
      if (trackText) {
        trackText.style.opacity = '1';
        trackText.innerHTML = `<span style="color:#ef4444; font-weight:700;">${isEn ? 'Chat Deleted!' : 'Chat Terhapus!'} 🗑️</span>`;
      }

      setTimeout(() => {
        deleteActiveChatFromNavbar();
        toggleSlideDelete(false);
      }, 350);
    } else {
      // Batal: reset slider
      resetSlideState();
    }
  }

  // Sentuhan (touch)
  thumb.addEventListener('touchstart', (e) => startDrag(e.touches[0].clientX), { passive: true });
  window.addEventListener('touchmove', (e) => {
    if (isDraggingSlide && e.touches[0]) moveDrag(e.touches[0].clientX);
  }, { passive: true });
  window.addEventListener('touchend', endDrag);

  // Mouse
  thumb.addEventListener('mousedown', (e) => {
    e.preventDefault();
    startDrag(e.clientX);
  });
  window.addEventListener('mousemove', (e) => {
    if (isDraggingSlide) moveDrag(e.clientX);
  });
  window.addEventListener('mouseup', endDrag);
}

function deleteActiveChatFromNavbar() {
  if (!activeSessionId || !sessions[activeSessionId]) return;
  const oldTitle = sessions[activeSessionId].title;
  delete sessions[activeSessionId];
  if (Object.keys(sessions).length === 0) {
    createNewChat(true);
  } else {
    activeSessionId = Object.keys(sessions)[0];
  }
  saveSessions();
  renderSessionsList();
  renderActiveSession();
  showToast(isEn ? `Deleted: "${oldTitle}"` : `Chat dihapus: "${oldTitle}"`);
}

// Input suara (speech recognition)
let speechRecognizer = null;
let isListeningSpeech = false;

function initSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) return;

  try {
    speechRecognizer = new SpeechRec();
    speechRecognizer.continuous = false;
    speechRecognizer.interimResults = true;

    speechRecognizer.onstart = () => {
      isListeningSpeech = true;
      const btn = document.getElementById('btn-mic');
      if (btn) btn.classList.add('listening');
      const input = document.getElementById('chat-input');
      if (input) {
        input.placeholder = isEn
          ? "Listening... Speak now nyaa~"
          : "Mendengarkan suara kamu... Bicaralah sekarang nyaa~";
      }
    };

    speechRecognizer.onresult = (event) => {
      let speechText = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        speechText += event.results[i][0].transcript;
      }
      const input = document.getElementById('chat-input');
      if (input && speechText) {
        input.value = speechText;
      }
    };

    speechRecognizer.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      stopSpeechListening();
      if (event.error === 'not-allowed') {
        showToast(isEn ? "Microphone permission blocked" : "Izin mikrofon diblokir oleh browser");
      } else if (event.error !== 'no-speech') {
        showToast(isEn ? `Mic error: ${event.error}` : `Kendala mic: ${event.error}`);
      }
    };

    speechRecognizer.onend = () => {
      stopSpeechListening();
    };
  } catch (err) {
    console.warn("SpeechRecognition init error:", err);
  }
}

function toggleSpeechRecognition() {
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    openAppModal({
      icon: 'ri-mic-off-line',
      iconType: 'info',
      badge: isEn ? 'BROWSER COMPATIBILITY' : 'KOMPATIBILITAS BROWSER',
      title: isEn ? 'Speech Recognition Unsupported' : 'Input Suara Belum Didukung',
      desc: isEn
        ? "Your current browser does not support the Web Speech API. For the best voice experience, please open this app in Google Chrome or Microsoft Edge."
        : "Browser yang kamu gunakan saat ini belum mendukung Web Speech API. Untuk mencoba fitur input suara, silakan buka aplikasi ini di Google Chrome atau Microsoft Edge ya!",
      showCallout: false,
      confirmText: isEn ? 'Got it' : 'Mengerti'
    });
    return;
  }

  if (isListeningSpeech) {
    if (speechRecognizer) {
      try { speechRecognizer.stop(); } catch (e) { }
    }
    stopSpeechListening();
  } else {
    if (!speechRecognizer) initSpeechRecognition();
    if (speechRecognizer) {
      speechRecognizer.lang = isEn ? 'en-US' : 'id-ID';
      try {
        speechRecognizer.start();
      } catch (e) {
        console.warn("Speech recognition start issue:", e);
      }
    }
  }
}

function stopSpeechListening() {
  isListeningSpeech = false;
  const btn = document.getElementById('btn-mic');
  if (btn) btn.classList.remove('listening');
  const input = document.getElementById('chat-input');
  if (input && remainingQuota > 0) {
    if (window.innerWidth <= 640) {
      input.placeholder = isEn ? "Ask Fetty anything... 🐾" : "Tanya seputar Fathi... 🐾";
    } else {
      input.placeholder = isEn ? "Ask anything about Fathi's projects, tech stack..." : "Ketik pertanyaan kamu seputar portofolio Fathi...";
    }
  }
}

// Kirim chat ke API
async function handleChatSubmit(e) {
  e.preventDefault();
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text || isGenerating) return;
  input.value = '';
  sendUserMessage(text);
}

async function sendUserMessage(text) {
  if (remainingQuota <= 0) {
    showQuotaExceededModal();
    return;
  }
  if (isGenerating) return;

  const sess = sessions[activeSessionId];
  if (!sess) return;

  // Sembunyikan hero
  document.getElementById('welcome-hero').style.display = 'none';

  const nowTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // Pesan user
  const userMsg = { role: 'user', content: text, time: nowTime };
  sess.messages.push(userMsg);
  appendMessageToDOM('user', text, nowTime);

  // Judul otomatis dari pesan pertama
  if (sess.title === "Chat Baru" || sess.title === "Obrolan Baru" || sess.title === "New Chat") {
    sess.title = text.length > 24 ? text.slice(0, 24) + '...' : text;
    document.getElementById('nav-session-title').textContent = sess.title;
    renderSessionsList();
  }

  sess.lang = isEn ? 'en' : 'id';
  saveSessions();
  recordQuestionUsage();

  // Loading indikator
  isGenerating = true;
  document.getElementById('btn-submit').disabled = true;
  const skeleton = document.getElementById('thinking-skeleton');
  skeleton.style.display = 'flex';
  scrollToBottom();

  try {
    // Riwayat pesan (filter error)
    const historyPayload = sess.messages.slice(0, -1)
      .filter(m => !m.isError)
      .map(m => ({
        role: m.role === 'assistant' ? 'model' : 'user',
        content: m.content
      }));

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: text,
        history: historyPayload,
        lang: isEn ? 'en' : 'id'
      })
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.message || `Server error (${res.status})`);
    }

    const data = await res.json();
    const replyText = data.reply || (isEn ? "No response received meow~ 😿" : "Tidak ada respon nyaa~ 😿");

    const botMsg = { role: 'assistant', content: replyText, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    sess.messages.push(botMsg);
    saveSessions();
    appendMessageToDOM('assistant', replyText, botMsg.time);
  } catch (err) {
    console.error(err);
    const errReply = isEn
      ? `Sorry meow 😿, there was an issue: ${err.message}. Please try again!`
      : `Waduh meow 😿, ada kendala: ${err.message}. Silakan coba lagi ya!`;
    const botMsg = { role: 'assistant', content: errReply, isError: true, time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
    sess.messages.push(botMsg);
    saveSessions();
    appendMessageToDOM('assistant', errReply, botMsg.time);
  } finally {
    isGenerating = false;
    skeleton.style.display = 'none';
    document.getElementById('btn-submit').disabled = false;
    scrollToBottom();
    document.getElementById('chat-input').focus();
  }
}

// Mulai aplikasi
window.onload = initApp;

window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeAppModal();
});

// Cek berkala jika waktu reset 12 jam tercapai saat user tetap membuka halaman
setInterval(() => {
  if (quotaResetAt && Date.now() >= quotaResetAt) {
    const wasExhausted = remainingQuota <= 0;
    checkAndResetQuota();
    updateQuotaUI();
    if (wasExhausted) {
      showToast(isEn ? "Your 5 chat questions quota has been reset!" : "Kuota 5 pertanyaan kamu telah direset kembali!");
    }
  }
}, 20000);
