"use client";
import { Dispatch, SetStateAction } from "react";
import Button from "../../components/ui/Button";
import { ConfigButton } from "./ConfigButton";
import { MicButton } from "./MicButton";

export function ChatInput({
  isPending,
  question,
  askQuestion,
  setQuestion,
}: {
  isPending: boolean;
  history: [string, string][];
  question: string;
  setQuestion: Dispatch<SetStateAction<string>>;
  askQuestion: () => Promise<void>;
}) {
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (!isPending) askQuestion();
      }}
      className="w-full flex items-center justify-center gap-2"
    >
      <textarea
        autoFocus
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // Prevents the newline from being entered in the textarea
            if (!isPending) askQuestion(); // Call the submit function here
          }
        }}
        className="w-full p-2 border border-gray-300 dark:border-gray-500 outline-none rounded dark:bg-gray-800"
        placeholder="Begin conversation here..."
      />
      <Button type="submit" isLoading={isPending}>
        {isPending ? "Thinking..." : "Chat"}
      </Button>
      <MicButton setQuestion={setQuestion} />
      <ConfigButton />
    </form>
  );
}
