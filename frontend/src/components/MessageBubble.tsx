import type { Message } from "../types";
import { BotAvatar, getCategoryIcon } from "./Icons";

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  if (isUser) {
    return (
      <div className="flex justify-end animate-fade-up">
        <div className="max-w-[80%] rounded-2xl rounded-br-md bg-gradient-to-br from-brand-600 to-accent-500 px-5 py-3.5 text-[15px] leading-6 text-white shadow-card">
          {message.content}
        </div>
      </div>
    );
  }

  return (
    <div className="flex gap-3 animate-fade-up">
      <BotAvatar />
      <div className="min-w-0 flex-1">
        <div className="rounded-2xl rounded-tl-md border border-white/60 bg-white/90 px-5 py-4 shadow-soft backdrop-blur-sm">
          <p className="whitespace-pre-wrap text-[15px] leading-7 text-ink-900">
            {message.content}
          </p>

          {message.sources && message.sources.length > 0 && (
            <div className="mt-4 border-t border-ink-100 pt-4">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-ink-500">
                Referenced topics
              </p>
              <div className="flex flex-wrap gap-2">
                {message.sources.map((source) => (
                  <span
                    key={`${source.category}-${source.question}`}
                    className="inline-flex items-center gap-1.5 rounded-full border border-brand-500/15 bg-brand-500/5 px-3 py-1.5 text-xs font-medium text-brand-700"
                  >
                    <span>{getCategoryIcon(source.category)}</span>
                    {source.category}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function TypingIndicator() {
  return (
    <div className="flex gap-3 animate-fade-up">
      <BotAvatar />
      <div className="flex items-center gap-2 rounded-2xl rounded-tl-md border border-white/60 bg-white/90 px-5 py-4 shadow-soft">
        <span className="h-2 w-2 animate-bounce rounded-full bg-brand-500" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-accent-500 delay-150" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-brand-400 delay-300" />
        <span className="ml-1 text-sm text-ink-500">Thinking...</span>
      </div>
    </div>
  );
}
