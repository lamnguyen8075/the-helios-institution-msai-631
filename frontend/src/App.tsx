import { useEffect, useState } from "react";
import { fetchExamples } from "./api/chat";
import { ChatWindow } from "./components/ChatWindow";

const FALLBACK_EXAMPLES = [
  "What are the admission requirements?",
  "How do I apply for financial aid?",
  "When is the scholarship application deadline?",
  "How do I register for classes?",
  "What student support services are available?",
];

export default function App() {
  const [examples, setExamples] = useState(FALLBACK_EXAMPLES);

  useEffect(() => {
    fetchExamples()
      .then((items) => {
        if (items.length > 0) {
          setExamples(items);
        }
      })
      .catch(() => undefined);
  }, []);

  return (
    <div className="mesh-bg min-h-screen">
      <ChatWindow examples={examples} />
    </div>
  );
}
