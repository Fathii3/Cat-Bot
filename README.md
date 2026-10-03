# Fetty Assistant - AI Portfolio Companion

Fetty Assistant adalah bot asisten portofolio interaktif berbasis kecerdasan buatan (Google Gemini) yang dibuat dengan Streamlit. Bot ini dirancang sebagai asisten virtual cerdas untuk menjawab berbagai pertanyaan seputar proyek, pengalaman kerja, sertifikasi, keahlian teknis, dan kontak dari Fathi Fadhil secara ramah dan profesional.

---

## Kegunaan & Manfaat

- Eksplorasi Portofolio Otomatis: Membantu pengunjung, klien, maupun perekrut (recruiter) memahami profil, pencapaian, dan arsitektur proyek developer tanpa harus membaca seluruh isi web secara manual.
- Tanya Jawab Konseptual & Teknis: Pengunjung dapat menanyakan latar belakang proyek, tantangan teknis yang dihadapi, solusi yang diterapkan, hingga tech stack spesifik.
- Penyedia Informasi Kontak: Memudahkan pengunjung yang ingin berkolaborasi atau menawarkan pekerjaan untuk mendapatkan tautan media sosial, email, dan nomor kontak resmi.
- Dapat Disematkan (Embeddable): Dirancang ringan dan responsif agar mudah dipasang sebagai widget chat mengambang atau modal iframe di situs web utama (fathifadhil.me).

---

## Fitur Utama

1. Persona Fetty:
   - Memiliki gaya komunikasi santai, sopan, dan hangat dengan persona ramah (meow~), namun tetap berbobot dan teknikal di mata profesional.
   - Mendukung dwibahasa: merespons dalam Bahasa Indonesia secara default, dan otomatis membalas dalam Bahasa Inggris jika ditanya dalam Bahasa Inggris.

2. Rotasi Multi-Key Cerdas (Hingga 5 API Key):
   - Mendukung input 1 hingga 5 Google Gemini API key di `.streamlit/secrets.toml`.
   - Menggunakan sistem rotasi proactive round-robin untuk membagi beban permintaan antar-key.
   - Dilengkapi proteksi cooldown otomatis 60 detik jika salah satu key terkena limit kuota (HTTP 429 RESOURCE_EXHAUSTED).

3. Prioritas Model Cepat & Ringan:
   - Mengutamakan model cepat generasi terbaru: `gemini-3.1-flash-lite` dan `gemini-3.5-flash-lite`, dengan fallback cadangan ke `gemini-3.6-flash` dan `gemini-flash-latest`.

4. Pintasan Topik Sekali Klik (st.pills):
   - Tersedia tombol pintasan topik instan: Projek, Sertifikat, Pengalaman, Tech, GitHub, dan Sosial Media.
   - Pengunjung bisa langsung bertanya dengan satu klik tanpa perlu mengetik dari awal.

5. Manajemen Riwayat Sesi Chat:
   - Pengunjung dapat membuat obrolan baru (Chat Baru), berpindah antar-sesi percakapan, atau menghapus sesi yang sudah tidak dibutuhkan.
   - Sesi diberi judul otomatis berdasarkan topik pesan pertama yang dikirim.

6. Antarmuka Modern & Responsif:
   - Tampilan skeleton loading shimmer saat Fetty sedang memproses jawaban.
   - Pesan informasi callout tip dan peringatan yang rapi.
   - Ikon vektor responsif dan tata letak optimal untuk perangkat mobile maupun desktop.

---

## Teknologi & Alat (Tech Stack)

| Komponen | Teknologi | Keterangan |
| :--- | :--- | :--- |
| Bahasa Utama | Python 3.13 | Python sistem + venv lokal (.venv) |
| Framework Web | Streamlit 1.65 | Framework aplikasi data dan antarmuka interaktif |
| Mesin AI | Google GenAI SDK | SDK resmi Google Gemini (google-genai) |
| Model AI | Gemini Flash Family | gemini-3.1-flash-lite, gemini-3.5-flash-lite |
| Knowledge Base | In-Memory RAG Context | Basis pengetahuan terstruktur di knowledge/portfolio_data.py |
| Ikonografi | Lucide SVG (Inlined) | Ikon vektor responsif tanpa dependensi eksternal |
| Styling | Scoped CSS | Desain modern beraksen hijau emerald (#059669) |

---

## Struktur Direktori

```text
Chat-bot/
  .streamlit/
    config.toml            # konfigurasi tema dan toolbar streamlit
    secrets.toml           # tempat menyimpan api key gemini (lokal, di-gitignore)
  assets/
    fetty_avatar.svg       # avatar maskot fetty
    user_avatar.svg        # avatar pengunjung
  components/
    __init__.py            # ekspor komponen
    icons.py               # kamus svg ikon lucide
    shortcuts.py           # widget pintasan topik (st.pills)
    ui.py                  # skeleton loading, callout, navbar, & brand
  knowledge/
    __init__.py
    portfolio_data.py      # sumber data keahlian, proyek, dan cv developer
  styles/
    __init__.py
    main_css.py            # styling antarmuka dan tema responsif
  utils/
    __init__.py
    gemini_manager.py      # manajemen api key, rotasi, cooldown, & prompt ai
    session_manager.py     # manajemen sesi dan histori percakapan (+ rate limiter)
  app.py                     # alur utama aplikasi streamlit
  requirements.txt           # daftar pustaka python
  README.md                  # dokumentasi proyek
```

---

## Panduan Instalasi & Menjalankan Aplikasi

Proyek ini memakai **virtual environment** (`.venv`) + **Python sistem 3.13**. Semua perintah di bawah dijalankan dari folder proyek (`D:\VC\Chat-bot`).

### 1. Setup pertama kali (sekali saja)

```powershell
cd D:\VC\Chat-bot
C:\Users\MP2NH\AppData\Local\Programs\Python\Python313\python.exe -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Konfigurasi API Key Gemini (lokal)

Berkas `.streamlit/secrets.toml` sudah ada di lokal (di-gitignore, jangan di-commit):

```toml
GEMINI_API_KEY_1 = "AQ.Ab8RN6J-..."
# GEMINI_API_KEY_2 = "AQ.Ab8RN6J-..."
GEMINI_API_KEY = "AQ.Ab8RN6J-..."
```

Tambah sampai 5 key untuk rotasi otomatis. Jangan pernah mengunggah berkas ini ke repositori publik.

### 3. Jalankan aplikasi (pemakaian harian)

Tanpa aktivasi (paling aman, anti salah interpreter):

```powershell
cd D:\VC\Chat-bot
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Atau dengan aktivasi dulu:

```powershell
cd D:\VC\Chat-bot
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Aplikasi terbuka di: `http://localhost:8501`.

> Catatan: `streamlit run app.py` polos TANPA venv/aktivasi pasti eror `streamlit is not recognized`. Jangan dipakai.

### 4. Sesuaikan Data Portofolio (opsional)

Buka `knowledge/portfolio_data.py`, ubah isi `PORTFOLIO_CONTEXT` sesuai data profil, riwayat kerja, proyek, dan kontak Anda.

### Troubleshooting

| Gejala | Penyebab & Solusi |
|---|---|
| `streamlit is not recognized` | Lupa pakai venv. Pakai `.\.venv\Scripts\python.exe -m streamlit run app.py` atau aktivasi dulu via `.\.venv\Scripts\Activate.ps1`. |
| `ModuleNotFoundError: No module named 'streamlit'` / `'google.genai'` | `python` polos menunjuk Python sistem yang kosong. Jangan `python app.py`, pakai path `.venv` di atas. |
| AI tidak merespons / error key | Cek `.streamlit/secrets.toml` ada dan key valid. Di Streamlit Cloud, isi ulang via dashboard: App > Settings > Secrets (file lokal tidak ikut deploy). |
| Port 8501 terpakai | Jalankan dengan port lain: `.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8502`. |

---

## Deploy ke Streamlit Cloud (gratis)

Lokal dan Cloud itu lingkungan terpisah. Cloud install sendiri dari `requirements.txt`, jadi hapus Anaconda / bikin `.venv` tidak berpengaruh ke deploy.

1. Push ke GitHub (`.venv/` dan `secrets.toml` otomatis di-ignore).
2. Di Streamlit Cloud: New app > pilih repo > `app.py`.
3. Isi Secrets via dashboard (App > Settings > Secrets), contoh:
```toml
GEMINI_API_KEY_1 = "AQ.Ab8RN6J-..."
GEMINI_API_KEY = "AQ.Ab8RN6J-..."
```
4. Deploy. Batas paket free: RAM kecil + app sleep saat idle — wajar, bukan error.

---

## Integrasi ke Web Portofolio (Iframe Embed)

Jika Anda memiliki situs web utama (misalnya menggunakan Next.js, React, atau HTML biasa), Anda dapat menyematkan asisten ini sebagai widget atau iframe:

```html
<iframe
  src="https://<nama-aplikasi-anda>.streamlit.app/?embed=true"
  style="width: 100%; height: 550px; border: none; border-radius: 16px;"
  title="Fetty Portfolio Companion"
  allow="clipboard-write"
></iframe>
```
