export function BrandLogo({ className = "h-8 w-8" }: { className?: string }) {
  return (
    <div
      className={`flex items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 via-accent-500 to-brand-600 shadow-glow ${className}`}
    >
      <svg viewBox="0 0 24 24" className="h-[55%] w-[55%]" fill="none" aria-hidden="true">
        <path
          d="M12 3L4 9v10h6v-6h4v6h6V9l-8-6z"
          fill="white"
          fillOpacity="0.95"
        />
      </svg>
    </div>
  );
}

export function BotAvatar({ className = "h-9 w-9" }: { className?: string }) {
  return (
    <div
      className={`flex shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500 to-accent-500 shadow-card ${className}`}
    >
      <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" aria-hidden="true">
        <path
          d="M9.5 8a2.5 2.5 0 115 0 2.5 2.5 0 01-5 0zM4 18c0-2.5 3.5-4 8-4s8 1.5 8 4"
          stroke="white"
          strokeWidth="1.8"
          strokeLinecap="round"
        />
        <path
          d="M12 2v2M5 5l1.5 1.5M19 5l-1.5 1.5"
          stroke="white"
          strokeWidth="1.5"
          strokeLinecap="round"
          opacity="0.7"
        />
      </svg>
    </div>
  );
}

export function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M5 12h14M13 6l6 6-6 6"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export function SparklesIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M9.5 2 8 8.5 1.5 10 8 11.5 9.5 18 11 11.5 17.5 10 11 11.5 9.5 2z" />
    </svg>
  );
}

const CATEGORY_ICONS: Record<string, string> = {
  admissions: "🎓",
  "academic programs": "📚",
  scholarships: "🏆",
  "financial aid": "💰",
  "student services": "🤝",
  enrollment: "📋",
  "campus life": "🏠",
  "international students": "🌍",
};

export function getCategoryIcon(category: string): string {
  return CATEGORY_ICONS[category.toLowerCase()] ?? "✨";
}
