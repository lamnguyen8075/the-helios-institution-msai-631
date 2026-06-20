export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Array<{
    category: string;
    question: string;
    score: number;
  }>;
}
