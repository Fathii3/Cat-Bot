import React, { useState, useRef, useEffect } from 'react';

/**
 * Jika portofolio kamu memiliki hook tema kustom (misal: useTheme dari NextThemes atau ThemeContext):
 * Kamu bisa meng-uncomment baris di bawah ini atau meneruskannya via props `isDark`.
 *
 * import { useTheme } from '@/hooks/useTheme'; // atau 'next-themes'
 */

// Tipe data pesan chat
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

// ============================================================================
// KONFIGURASI PENGHUBUNG KE REPO CHAT-BOT (VERCEL BACKEND)
// Masukkan domain Vercel hasil deploy dari repositori Chat-bot ini.
// Contoh: "https://cat-bot-fathi.vercel.app/api/chat"
// Komponen ini juga otomatis membaca variabel VITE_CHAT_API_URL jika disetel di .env portfolio.
// ============================================================================
const DEFAULT_REMOTE_API_URL = 'https://cat-bot-fathi.vercel.app/api/chat';

function resolveApiEndpoint(): string {
  try {
    // @ts-ignore
    if (typeof import.meta !== 'undefined' && import.meta.env?.VITE_CHAT_API_URL) {
      // @ts-ignore
      return import.meta.env.VITE_CHAT_API_URL;
    }
  } catch (_) {}

  try {
    if (typeof process !== 'undefined' && process.env?.NEXT_PUBLIC_CHAT_API_URL) {
      return process.env.NEXT_PUBLIC_CHAT_API_URL;
    }
  } catch (_) {}

  return DEFAULT_REMOTE_API_URL;
}

const CHAT_API_ENDPOINT = resolveApiEndpoint();


// Pesan sambutan awal dari Cat-Bot (Neko)
const INITIAL_MESSAGE: ChatMessage = {
  id: 'init-greeting',
  role: 'assistant',
  content:
    'Halo nyaa~! 🐾 Aku Cat-Bot (Neko), maskot asisten portofolio resmi Fathi Fadhil. Mau tanya seputar proyek unggulan, keahlian tech stack, atau cara berkolaborasi dengan Fathi? Silakan tanyakan meow~!',
  timestamp: new Date(),
};

// Rekomendasi pertanyaan cepat (quick prompts)
const QUICK_PROMPTS = [
  'Apa saja proyek unggulan Fathi? 🚀',
  'Tech stack yang dikuasai Fathi? 💻',
  'Bagaimana cara menghubungi Fathi? 📬',
];

export interface CatBubbleCompanionProps {
  /**
   * Opsional: Override URL endpoint API serverless (misal: "https://cat-bot.vercel.app/api/chat")
   */
  apiUrl?: string;

  /**
   * Opsional: Status tema dari hook `useTheme` jika ingin dipassing secara eksplisit
   */
  isDark?: boolean;
}

export const CatBubbleCompanion: React.FC<CatBubbleCompanionProps> = ({ apiUrl }) => {
  // Opsional jika proyek memiliki hook useTheme:
  // const { theme } = useTheme?.() || { theme: 'light' };
  // const isDarkMode = isDark !== undefined ? isDark : theme === 'dark';

  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([INITIAL_MESSAGE]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const activeApiUrl = apiUrl || CHAT_API_ENDPOINT;

  // Auto-scroll ke pesan paling bawah saat ada pembaruan
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
      setUnreadCount(0);
      setTimeout(() => inputRef.current?.focus(), 150);
    }
  }, [isOpen, messages, isLoading]);

  // Handler kirim pesan chat
  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend ?? inputValue).trim();
    if (!text || isLoading) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // Format chat history untuk percakapan multi-turn kontekstual
      const historyPayload = updatedMessages
        .filter((m) => m.id !== 'init-greeting')
        .map((m) => ({
          role: m.role === 'assistant' ? 'model' : 'user',
          content: m.content,
        }));

      const response = await fetch(activeApiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: text,
          history: historyPayload,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `Gagal menghubungi server (${response.status})`
        );
      }

      const data = await response.json();
      const botReply =
        data.reply || 'Maaf meow, Neko tidak menerima respons dari server nyaa~ 😿';

      const assistantMessage: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: botReply,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (!isOpen) {
        setUnreadCount((c) => c + 1);
      }
    } catch (error: any) {
      console.error('Cat-Bot Error:', error);
      const errorMessage: ChatMessage = {
        id: `err-${Date.now()}`,
        role: 'assistant',
        content: `Meoww 😿 Terjadi kendala teknis: ${
          error.message || 'Koneksi terputus'
        }. Silakan coba kirim lagi ya nyaa~!`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Reset riwayat chat ke pesan default
  const handleResetChat = () => {
    if (window.confirm('Hapus riwayat obrolan dan mulai baru nyaa~?')) {
      setMessages([INITIAL_MESSAGE]);
      setInputValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="fixed bottom-5 right-5 z-50 flex flex-col items-end font-sans">
      {/* Jendela Modal Chat Native */}
      {isOpen && (
        <div
          role="dialog"
          aria-label="Cat-Bot AI Assistant Chat"
          className="w-[92vw] sm:w-[400px] h-[550px] max-h-[85vh] bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-3xl shadow-2xl overflow-hidden mb-3 flex flex-col relative animate-in fade-in slide-in-from-bottom-5 duration-200 transition-colors"
        >
          {/* Header Bar */}
          <div className="bg-gradient-to-r from-emerald-600 via-emerald-700 to-teal-700 text-white px-4 py-3 flex justify-between items-center z-10 shadow-sm shrink-0">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-full bg-white/20 flex items-center justify-center text-xl shadow-inner">
                🐱
              </div>
              <div>
                <h3 className="text-sm font-bold leading-tight flex items-center gap-1.5">
                  Cat-Bot (Neko)
                  <span className="inline-block w-2 h-2 rounded-full bg-emerald-300 animate-pulse" />
                </h3>
                <p className="text-[11px] text-emerald-100/90">
                  Asisten Portofolio Fathi Fadhil
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              {/* Tombol Clear/Reset Chat */}
              <button
                type="button"
                onClick={handleResetChat}
                className="p-1.5 text-emerald-100 hover:text-white hover:bg-white/10 rounded-lg transition-colors text-xs flex items-center gap-1"
                title="Hapus riwayat obrolan"
                aria-label="Hapus riwayat obrolan"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
              </button>

              {/* Tombol Tutup Modal */}
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 text-emerald-100 hover:text-white hover:bg-white/10 rounded-lg transition-colors text-lg font-bold leading-none"
                aria-label="Tutup Obrolan"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Area Daftar Pesan Chat */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3.5 bg-zinc-50 dark:bg-zinc-950/60 scroll-smooth">
            {messages.map((msg) => {
              const isAssistant = msg.role === 'assistant';
              return (
                <div
                  key={msg.id}
                  className={`flex gap-2.5 items-end ${
                    isAssistant ? 'justify-start' : 'justify-end'
                  }`}
                >
                  {isAssistant && (
                    <div className="w-7 h-7 rounded-full bg-emerald-100 dark:bg-emerald-950/70 border border-emerald-300 dark:border-emerald-800 flex items-center justify-center text-xs shrink-0 select-none shadow-sm">
                      🐾
                    </div>
                  )}

                  <div
                    className={`max-w-[78%] px-3.5 py-2.5 rounded-2xl text-xs sm:text-[13px] leading-relaxed shadow-sm transition-colors ${
                      isAssistant
                        ? 'bg-white dark:bg-zinc-800 text-zinc-800 dark:text-zinc-100 border border-zinc-200/80 dark:border-zinc-700/80 rounded-bl-xs'
                        : 'bg-emerald-600 dark:bg-emerald-700 text-white rounded-br-xs'
                    }`}
                  >
                    <div className="whitespace-pre-wrap break-words">{msg.content}</div>
                    <div
                      className={`text-[9px] mt-1 text-right select-none ${
                        isAssistant
                          ? 'text-zinc-400 dark:text-zinc-400'
                          : 'text-emerald-200'
                      }`}
                    >
                      {new Date(msg.timestamp).toLocaleTimeString([], {
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </div>
                  </div>
                </div>
              );
            })}

            {/* Animasi Loading / Mengetik (Typing Indicator) */}
            {isLoading && (
              <div className="flex gap-2.5 items-end justify-start">
                <div className="w-7 h-7 rounded-full bg-emerald-100 dark:bg-emerald-950/70 border border-emerald-300 dark:border-emerald-800 flex items-center justify-center text-xs shrink-0 select-none">
                  🐾
                </div>
                <div className="bg-white dark:bg-zinc-800 border border-zinc-200/80 dark:border-zinc-700/80 rounded-2xl rounded-bl-xs px-3.5 py-2.5 shadow-sm flex items-center gap-1.5">
                  <span className="text-[11px] text-zinc-500 dark:text-zinc-400 mr-1">
                    Neko sedang berpikir nyaa~
                  </span>
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-bounce [animation-delay:-0.3s]" />
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-bounce [animation-delay:-0.15s]" />
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-bounce" />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Prompt Chips Cepat */}
          {messages.length === 1 && !isLoading && (
            <div className="px-3 py-2 bg-zinc-100/70 dark:bg-zinc-900/90 border-t border-zinc-200/60 dark:border-zinc-800/60 flex flex-wrap gap-1.5 shrink-0">
              {QUICK_PROMPTS.map((prompt, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSendMessage(prompt)}
                  className="text-[11px] bg-white dark:bg-zinc-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/50 text-zinc-700 dark:text-zinc-300 hover:text-emerald-700 dark:hover:text-emerald-300 border border-zinc-200 dark:border-zinc-700 px-2.5 py-1 rounded-full transition-all duration-150 cursor-pointer shadow-2xs"
                >
                  {prompt}
                </button>
              ))}
            </div>
          )}

          {/* Form Input Pesan */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="p-2.5 bg-white dark:bg-zinc-900 border-t border-zinc-200 dark:border-zinc-800 flex items-center gap-2 shrink-0"
          >
            <input
              ref={inputRef}
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              placeholder="Tanya seputar Fathi nyaa... 🐾"
              className="flex-1 bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 text-xs sm:text-[13px] px-3.5 py-2.5 rounded-xl border border-transparent focus:border-emerald-500 dark:focus:border-emerald-500 focus:bg-white dark:focus:bg-zinc-800 outline-none transition-all disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className="w-9 h-9 flex items-center justify-center bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl shadow-sm transition-all duration-150 disabled:opacity-40 disabled:cursor-not-allowed hover:scale-105 active:scale-95 shrink-0"
              aria-label="Kirim Pesan"
            >
              <svg
                className="w-4 h-4 translate-x-0.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </button>
          </form>
        </div>
      )}

      {/* Floating Action Button (Maskot Kucing Neko) */}
      <button
        type="button"
        onClick={() => setIsOpen((prev) => !prev)}
        className="group relative flex items-center justify-center w-14 h-14 bg-gradient-to-tr from-emerald-600 to-teal-500 hover:from-emerald-700 hover:to-teal-600 text-white rounded-full shadow-xl hover:shadow-2xl hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer"
        aria-label={isOpen ? 'Tutup Cat-Bot' : 'Buka Asisten Cat-Bot (Neko)'}
      >
        <span className="text-2xl transition-transform duration-200 group-hover:scale-110">
          {isOpen ? '🐾' : '🐱'}
        </span>

        {/* Badge status notifikasi */}
        {!isOpen && (
          <span className="absolute -top-1 -right-1 flex h-4 w-4">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex items-center justify-center rounded-full h-4 w-4 bg-emerald-500 text-[9px] font-bold text-white">
              {unreadCount > 0 ? unreadCount : '•'}
            </span>
          </span>
        )}
      </button>
    </div>
  );
};

export default CatBubbleCompanion;
