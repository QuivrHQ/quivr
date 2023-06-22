/* eslint-disable */
"use client";
import Button from "@/lib/components/ui/Button";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useState } from "react";
import { ConfigButton } from "./ConfigButton";
import { MicButton } from "./MicButton";

export const ChatInput = (): JSX.Element => {
  const [message, setMessage] = useState<string>(""); // for optimistic updates
  const { addQuestion, generatingAnswer } = useChat();

  const submitQuestion = () => {
    addQuestion(message, () => setMessage(""));
  };
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (!generatingAnswer) {
          submitQuestion();
        }
      }}
      className="sticky bottom-0 p-5 bg-white dark:bg-black rounded-t-md border border-black/10 dark:border-white/25 border-b-0 w-full max-w-3xl flex items-center justify-center gap-2 z-20"
    >
      <textarea
        autoFocus
        value={message}
        required
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (message.length === 0) return;
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // Prevents the newline from being entered in the textarea
            if (!generatingAnswer) {
              submitQuestion();
            }
          }
        }}
        className="w-full p-2 border border-gray-300 dark:border-gray-500 outline-none rounded dark:bg-gray-800"
        placeholder="Begin conversation here..."
      />
      <Button
        className="px-3 py-2 sm:px-4 sm:py-2"
        type="submit"
        isLoading={generatingAnswer}
      >
        {generatingAnswer ? "Thinking..." : "Chat"}
      </Button>
      <div className="flex items-center">
        <MicButton setMessage={setMessage} />
        <ConfigButton />
      </div>
    </form>
  );
};
