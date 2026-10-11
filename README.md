# Cat-Bot (Neko) - Vercel Serverless AI Service & React Widget

Layanan AI Serverless dan komponen antarmuka chat portofolio untuk **Fathi Fadhil** ([fathifadhil.me](https://fathifadhil.me)) bertenaga **Google Gemini API (`gemini-1.5-flash`)** yang di-host di **Vercel Serverless Function**.

---

## 🏗️ Arsitektur 2-Repository (Terpisah)

```
┌────────────────────────────────────────────────────────┐
│ REPO 1: Portfolio Web (fathifadhil.me)                 │
│ Framework: React (Vite / SPA) + TypeScript + Tailwind  │
│ Komponen: src/components/ui/CatBubbleCompanion.tsx     │
│ Hosting: Vercel                                        │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP POST /api/chat
                           ▼
┌────────────────────────────────────────────────────────┐
│ REPO 2: Cat-Bot Service (Repo Ini: Chat-bot)           │
│ Runtime: Node.js / TypeScript Serverless Function      │
│ Endpoint: /api/chat.ts                                 │
│ Model: Google Gemini API (gemini-1.5-flash)            │
│ Hosting: Vercel (Standalone Serverless Project)        │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Struktur Direktori Repo `Chat-bot`

```
Chat-bot/
├── api/
│   ├── chat.ts               # Vercel Serverless Function (POST handler + Gemini API)
│   └── knowledge.ts          # Knowledge Base resmi Fathi Fadhil untuk context AI
├── src/
│   └── components/
│       └── ui/
│           └── CatBubbleCompanion.tsx # Komponen React Native untuk dipasang di Portfolio
├── vercel.json               # Konfigurasi CORS & Vercel routing
├── package.json              # Dependensi Google GenAI SDK & TypeScript
├── tsconfig.json             # Konfigurasi TypeScript
├── .env.example              # Template environment variable
└── README.md
```

---

## 🚀 Panduan Setup & Deploy

### Langkah 1: Deploy Repo `Chat-bot` ke Vercel

1. **Push perubahan repo ini ke GitHub:**
   ```bash
   git add .
   git commit -m "feat: migrate chatbot to Vercel Serverless Function with Gemini 1.5 Flash"
   git push origin main
   ```
2. Buka dashboard [Vercel](https://vercel.com/) -> **Add New Project**.
3. Import repositori **`Cat-Bot`**.
4. Di bagian **Environment Variables**, tambahkan:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** API key Gemini kamu (dapatkan dari [Google AI Studio](https://aistudio.google.com/)).
5. Klik **Deploy**. Setelah selesai, kamu akan mendapatkan domain Vercel (misal: `https://cat-bot-api.vercel.app`).

---

### Langkah 2: Pasang Komponen di Proyek Portofolio React (fathifadhil.me)

1. Salin file `src/components/ui/CatBubbleCompanion.tsx` dari repo ini ke folder `src/components/ui/CatBubbleCompanion.tsx` di repo portofolio kamu.
2. Tambahkan environment variable di file `.env` proyek portofolio kamu:
   ```env
   VITE_CHAT_API_URL=https://<nama-project-vercel-kamu>.vercel.app/api/chat
   ```
   *(Atau gunakan fitur Vercel Rewrites jika ingin memanggil `/api/chat` secara relatif).*
3. Pasang komponen di halaman utama (misal `App.tsx` atau layout utama):
   ```tsx
   import { CatBubbleCompanion } from './components/ui/CatBubbleCompanion';

   export default function App() {
     return (
       <div>
         {/* Konten Portofolio */}
         <CatBubbleCompanion />
       </div>
     );
   }
   ```

---

## 🔒 Konfigurasi Vercel Rewrites (Opsional)

Jika ingin memanggil `/api/chat` tanpa mencantumkan full URL di frontend, tambahkan rewrite di `vercel.json` repo portofolio kamu:

```json
{
  "rewrites": [
    {
      "source": "/api/chat",
      "destination": "https://<nama-project-cat-bot>.vercel.app/api/chat"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```
