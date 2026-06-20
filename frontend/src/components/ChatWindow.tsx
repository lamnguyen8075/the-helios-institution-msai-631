import { FormEvent, useEffect, useRef, useState } from "react";
import { sendMessage } from "../api/chat";
import type { Message } from "../types";
import { BrandLogo, SendIcon } from "./Icons";
import { MessageBubble, TypingIndicator } from "./MessageBubble";
import { WelcomeScreen } from "./WelcomeScreen";

interface ChatWindowProps {
  examples: string[];
}

function createId() {
  return crypto.randomUUID();
}

export function ChatWindow({ examples }: ChatWindowProps) {
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const isWelcome = messages.length === 0 && !loading;

  useEffect(() => {
    if (!isWelcome) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, loading, isWelcome]);

  useEffect(() => {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 120)}px`;
  }, [draft]);

  async function handleSubmit(event?: FormEvent, preset?: string) {
    event?.preventDefault();
    const trimmed = (preset ?? draft).trim();
    if (!trimmed || loading) return;

    const userMessage: Message = {
      id: createId(),
      role: "user",
      content: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setDraft("");
    setLoading(true);

    try {
      const response = await sendMessage(trimmed);
      setMessages((prev) => [
        ...prev,
        {
          id: createId(),
          role: "assistant",
          content: response.answer,
          sources: response.sources,
        },
      ]);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Something went wrong. Please try again.";
      setMessages((prev) => [
        ...prev,
        {
          id: createId(),
          role: "assistant",
          content: message,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function clearConversation() {
    setDraft("");
    setMessages([]);
  }

  return (
    <div className="relative flex h-screen flex-col">
      {/* ambient orbs */}
      <div className="pointer-events-none absolute left-[10%] top-[15%] h-64 w-64 rounded-full bg-brand-500/10 blur-3xl animate-float" />
      <div className="pointer-events-none absolute bottom-[20%] right-[8%] h-72 w-72 rounded-full bg-accent-500/10 blur-3xl animate-float [animation-delay:2s]" />

      {/* top bar */}
      <header className="relative z-10 flex items-center justify-between px-5 py-4 md:px-8">
        <div className="flex items-center gap-3">
          <BrandLogo className="h-9 w-9 rounded-xl" />
          <div>
            <p className="text-sm font-bold text-ink-900">Campus AI</p>
            <p className="text-xs text-ink-500">University Support</p>
          </div>
        </div>

        {messages.length > 0 && (
          <button
            type="button"
            onClick={clearConversation}
            className="rounded-full border border-brand-500/20 bg-white/80 px-4 py-2 text-sm font-semibold text-brand-600 shadow-sm backdrop-blur-sm transition hover:bg-white hover:shadow-soft"
          >
            + New chat
          </button>
        )}
      </header>

      {/* messages */}
      <div className="relative z-10 flex-1 overflow-y-auto">
        {isWelcome ? (
          <WelcomeScreen
            examples={examples}
            onSelect={(example) => void handleSubmit(undefined, example)}
            disabled={loading}
          />
        ) : (
          <div className="mx-auto w-full max-w-3xl space-y-5 px-5 py-4 md:px-8">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {loading && <TypingIndicator />}
            <div ref={bottomRef} className="h-6" />
          </div>
        )}
      </div>

      {/* input dock */}
      <div className="relative z-10 px-5 pb-6 pt-2 md:px-8">
        <form
          onSubmit={handleSubmit}
          className="gradient-border mx-auto flex w-full max-w-3xl items-end gap-3 rounded-[24px] bg-white/90 px-4 py-3 shadow-dock backdrop-blur-xl transition focus-within:shadow-glow"
        >
          <textarea
            ref={textareaRef}
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                void handleSubmit();
              }
            }}
            rows={1}
            placeholder="Ask anything about your university..."
            className="max-h-[120px] min-h-[28px] flex-1 resize-none bg-transparent text-[15px] leading-6 text-ink-900 outline-none placeholder:text-ink-500"
          />

          <button
            type="submit"
            disabled={loading || !draft.trim()}
            aria-label="Send message"
            className="mb-0.5 flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-brand-600 to-accent-500 text-white shadow-card transition hover:brightness-110 disabled:opacity-30"
          >
            <SendIcon />
          </button>
        </form>

        <p className="mx-auto mt-3 max-w-3xl text-center text-xs text-ink-500">
          Powered by open-source AI · Answers grounded in university FAQs
        </p>
      </div>
    </div>
  );
}
