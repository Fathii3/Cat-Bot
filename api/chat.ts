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

// Helper untuk mengambil seluruh API key dari environment (GEMINI_API_KEY_1..5 atau GEMINI_API_KEY)
function getGeminiApiKeys(): string[] {
  const keys: string[] = [];

  // Cek nomor 1 sampai 9
  for (let i = 1; i <= 9; i++) {
    const k = process.env[`GEMINI_API_KEY_${i}`]?.trim();
    if (k && !keys.includes(k)) {
      keys.push(k);
    }
  }

  // Cek kunci tunggal
  const single = process.env.GEMINI_API_KEY?.trim();
  if (single && !keys.includes(single)) {
    keys.push(single);
  }

  return keys;
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
  const apiKeys = getGeminiApiKeys();
  if (apiKeys.length === 0) {
    console.error('Server Configuration Error: Belum ada GEMINI_API_KEY atau GEMINI_API_KEY_1..5 yang disetel.');
    return res.status(500).json({
      error: 'Missing API Key',
      message: 'Belum ada GEMINI_API_KEY atau GEMINI_API_KEY_1..5 yang dikonfigurasi di environment Vercel.',
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

    // 6. Format Multi-Turn Chat History
    const formattedHistory: Array<{
      role: 'user' | 'model';
      parts: Array<{ text: string }>;
    }> = [];

    if (Array.isArray(history)) {
      for (const item of history) {
        if (!item) continue;
        const textContent = (item.content || item.text || '').trim();
        if (!textContent) continue;

        const role: 'user' | 'model' =
          item.role === 'assistant' || item.role === 'model' ? 'model' : 'user';

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

    // 7. Eksekusi obrolan dengan rotasi / failover otomatis antar-API Key
    let responseText: string | null = null;
    let lastError: any = null;

    const CANDIDATE_MODELS = [
      'gemini-3.5-flash-lite',
      'gemini-3.1-flash-lite',
    ];

    for (let i = 0; i < apiKeys.length; i++) {
      const currentKey = apiKeys[i];
      const genAI = new GoogleGenerativeAI(currentKey);

      for (const modelName of CANDIDATE_MODELS) {
        try {
          const model = genAI.getGenerativeModel({
            model: modelName,
            systemInstruction: BASE_SYSTEM_INSTRUCTION,
            generationConfig: {
              temperature: 0.3,
              topP: 0.95,
              maxOutputTokens: 1000,
            },
          });

          const chat = model.startChat({
            history: formattedHistory,
          });

          const result = await chat.sendMessage(userMessage);
          responseText = result.response.text();

          if (responseText) {
            break; // Berhasil mendapatkan jawaban!
          }
        } catch (err: any) {
          lastError = err;
          console.warn(`Model ${modelName} dengan key index ${i} gagal: ${err?.message}`);
        }
      }

      if (responseText) {
        break; // Berhasil, keluar dari loop key
      }
    }


    if (!responseText) {
      throw lastError || new Error('Semua API key gagal memproses respons.');
    }

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
