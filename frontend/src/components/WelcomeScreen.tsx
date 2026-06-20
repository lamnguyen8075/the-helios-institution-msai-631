import { BrandLogo, SparklesIcon } from "./Icons";

const PROMPT_META = [
  { icon: "🎓", label: "Admissions" },
  { icon: "💰", label: "Financial Aid" },
  { icon: "🏆", label: "Scholarships" },
  { icon: "📋", label: "Enrollment" },
  { icon: "🤝", label: "Student Services" },
];

interface WelcomeScreenProps {
  examples: string[];
  onSelect: (example: string) => void;
  disabled?: boolean;
}

export function WelcomeScreen({ examples, onSelect, disabled }: WelcomeScreenProps) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-6 pb-10 pt-8">
      <div className="animate-fade-up text-center">
        <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center">
          <BrandLogo className="h-16 w-16 rounded-2xl" />
        </div>

        <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-brand-500/20 bg-brand-500/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-brand-600">
          <SparklesIcon />
          AI-Powered Support
        </div>

        <h1 className="text-4xl font-bold tracking-tight md:text-5xl">
          <span className="gradient-text">Helios answers,</span>
          <br />
          instantly.
        </h1>
        <p className="mx-auto mt-4 max-w-lg text-base leading-relaxed text-ink-500">
          Your personal Helios Institution assistant for admissions, aid, scholarships,
          and student services — grounded in real FAQ data.
        </p>
      </div>

      <div className="mt-8 flex flex-wrap justify-center gap-2 animate-fade-up">
        {PROMPT_META.map((item) => (
          <span
            key={item.label}
            className="rounded-full border border-white/80 bg-white/70 px-3 py-1.5 text-xs font-medium text-ink-700 shadow-sm backdrop-blur-sm"
          >
            {item.icon} {item.label}
          </span>
        ))}
      </div>

      <div className="mt-10 grid w-full max-w-2xl grid-cols-1 gap-3 sm:grid-cols-2">
        {examples.map((example, index) => (
          <button
            key={example}
            type="button"
            disabled={disabled}
            onClick={() => onSelect(example)}
            style={{ animationDelay: `${index * 60}ms` }}
            className="group gradient-border animate-fade-up rounded-2xl bg-white/80 p-5 text-left shadow-soft backdrop-blur-sm transition hover:-translate-y-1 hover:bg-white hover:shadow-glow disabled:opacity-50"
          >
            <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-brand-500/10 to-accent-500/10 text-lg transition group-hover:from-brand-500/20 group-hover:to-accent-500/20">
              {PROMPT_META[index % PROMPT_META.length]?.icon ?? "💬"}
            </div>
            <p className="text-sm font-semibold leading-snug text-ink-900">{example}</p>
            <p className="mt-2 text-xs font-medium text-brand-600 opacity-0 transition group-hover:opacity-100">
              Ask this →
            </p>
          </button>
        ))}
      </div>
    </div>
  );
}
