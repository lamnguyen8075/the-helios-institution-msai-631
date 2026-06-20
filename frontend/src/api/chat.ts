export interface SourceItem {
  category: string;
  question: string;
  score: number;
}

export interface ChatResponse {
  answer: string;
  sources: SourceItem[];
}

const API_BASE = import.meta.env.VITE_API_BASE ?? "";

export async function sendMessage(message: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail ?? "Unable to reach the assistant.");
  }

  return response.json();
}

export async function fetchExamples(): Promise<string[]> {
  const response = await fetch(`${API_BASE}/api/examples`);
  if (!response.ok) {
    return [];
  }
  const data = await response.json();
  return data.examples ?? [];
}
