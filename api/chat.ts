import type { VercelRequest, VercelResponse } from '@vercel/node';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { PORTFOLIO_KNOWLEDGE } from './knowledge';

// Interface untuk item riwayat pesan yang dikirim dari klien
export interface ChatHistoryItem {
  role: 'user' | 'model' | 'assistant';
  content?: string;
  text?: string;
}

// System Instruction persona Cat-Bot (Neko)
const BASE_SYSTEM_INSTRUCTION = `Kamu adalah Cat-Bot (Neko), maskot asisten portofolio Fathi Fadhil yang ramah, sopan, sedikit jenaka dengan ekspresi kucing ('nyaa~'). Kamu bertugas menjawab pertanyaan pengunjung seputar keahlian, proyek, dan latar belakang Fathi Fadhil.

Pedoman Komunikasi:
1. Karakter: Ramah, antusias, solutif, sedikit jenaka dengan sisipan ekspresi kucing yang lucu dan sopan ('nyaa~', 'meow!', emoji 🐾/🐱), namun tetap profesional dan berwibawa di mata recruiter atau klien.
2. Bahasa: Gunakan bahasa yang sama dengan pengunjung (Bahasa Indonesia santai-profesional secara default, atau Bahasa Inggris yang natural jika pengunjung bertanya dalam bahasa Inggris).
3. Batasan Topik (Guardrails): Fokus HANYA pada informasi seputar Fathi Fadhil, portofolio, proyek, keahlian teknis (tech stack), pengalaman, sertifikasi, dan kontak kolaborasi. Jika ditanya di luar topik (resep masakan, politik, tugas umum, dsb), tolak secara halus dan jenaka dengan gaya kucing ('Maaf meow, Neko hanya bisa menjawab seputar portofolio dan proyek Fathi Fadhil nyaa~ 🐾').
4. Fakta: Jawab berdasarkan data resmi Knowledge Base berikut. Jangan pernah mengarang data atau proyek yang tidak tercantum. Jawab secara ringkas, padat, dan jelas (3-5 kalimat kecuali jika pengunjung meminta penjelasan teknis mendalam).

=== KNOWLEDGE BASE PORTOFOLIO FATHI FADHIL ===
${PORTFOLIO_KNOWLEDGE}
`;

// Helper untuk menyetel CORS header
function setCorsHeaders(req: VercelRequest, res: VercelResponse) {
  const allowedOrigins = [
    'https://fathifadhil.me',
    'https://www.fathifadhil.me',
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:4173',
  ];

  const origin = req.headers.origin as string | undefined;
  if (origin && (allowedOrigins.includes(origin) || origin.endsWith('.vercel.app'))) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  } else {
    res.setHeader('Access-Control-Allow-Origin', '*');
  }

  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'Content-Type, Authorization, X-Requested-With'
  );
  res.setHeader('Access-Control-Allow-Credentials', 'true');
}

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // 1. Tangani CORS Headers
  setCorsHeaders(req, res);

  // 2. Tangani Preflight OPTIONS Request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // 3. Hanya izinkan metode POST
  if (req.method !== 'POST') {
    return res.status(405).json({
      error: 'Method Not Allowed',
      message: 'Endpoint ini hanya menerima permintaan HTTP POST.',
    });
  }

  // 4. Verifikasi GEMINI_API_KEY di environment
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    console.error('Server Configuration Error: GEMINI_API_KEY belum disetel.');
    return res.status(500).json({
      error: 'Missing API Key',
      message: 'GEMINI_API_KEY belum dikonfigurasi di environment Vercel serverless.',
    });
  }

  try {
    // 5. Ekstraksi request body
    const { message, history } = req.body || {};

    if (!message || typeof message !== 'string' || !message.trim()) {
      return res.status(400).json({
        error: 'Bad Request',
        message: 'Field "message" wajib diisi dengan string non-kosong.',
      });
    }

    const userMessage = message.trim();

    // 6. Inisialisasi Google Gemini AI Client
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: 'gemini-1.5-flash',
      systemInstruction: BASE_SYSTEM_INSTRUCTION,
      generationConfig: {
        temperature: 0.3,
        topP: 0.95,
        maxOutputTokens: 1000,
      },
    });

    // 7. Format Multi-Turn Chat History
    const formattedHistory: Array<{
      role: 'user' | 'model';
      parts: Array<{ text: string }>;
    }> = [];

    if (Array.isArray(history)) {
      for (const item of history) {
        if (!item) continue;
        const rawRole = (item.role || '').toLowerCase();
        const textContent = (item.content || item.text || '').trim();

        if (!textContent) continue;

        // Normalisasi role: 'user' -> 'user', 'assistant'/'model' -> 'model'
        const role: 'user' | 'model' =
          rawRole === 'assistant' || rawRole === 'model' ? 'model' : 'user';

        formattedHistory.push({
          role,
          parts: [{ text: textContent }],
        });
      }
    }

    // Pastikan percakapan Gemini dimulai dengan giliran 'user'
    while (formattedHistory.length > 0 && formattedHistory[0].role !== 'user') {
      formattedHistory.shift();
    }

    // 8. Eksekusi obrolan multi-turn dengan Gemini API
    const chat = model.startChat({
      history: formattedHistory,
    });

    const result = await chat.sendMessage(userMessage);
    const responseText = result.response.text();

    return res.status(200).json({
      reply: responseText,
      status: 'success',
    });
  } catch (error: any) {
    console.error('Error saat memproses chat dengan Gemini:', error);

    const errorMessage = error?.message || 'Terjadi kesalahan internal pada server.';
    const statusCode = error?.status || 500;

    return res.status(statusCode).json({
      error: 'AI_GENERATION_FAILED',
      message: errorMessage,
    });
  }
}
