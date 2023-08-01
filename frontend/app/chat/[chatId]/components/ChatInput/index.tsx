/* eslint-disable */
"use client";
import Button from "@/lib/components/ui/Button";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useState } from "react";
import { ConfigModal } from "./components/ConfigModal";
import { MicButton } from "./components/MicButton/MicButton";

export const ChatInput = (): JSX.Element => {
  const [message, setMessage] = useState<string>("");
  const { addQuestion, generatingAnswer, chatId } = useChat();

  const submitQuestion = () => {
    if (message.length === 0) return;
    if (!generatingAnswer) {
      addQuestion(message, () => setMessage(""));
    }
  };

  return (
    <form
      data-testid="chat-input-form"
      onSubmit={(e) => {
        e.preventDefault();
        submitQuestion();
      }}
      className="sticky bottom-0 p-5 bg-white dark:bg-black rounded-t-md border border-black/10 dark:border-white/25 border-b-0 w-full max-w-3xl flex items-center justify-center gap-2 z-20"
    >
      <textarea
        autoFocus
        value={message}
        required
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // Prevents the newline from being entered in the textarea
            submitQuestion();
          }
        }}
        className="w-full p-2 border border-gray-300 dark:border-gray-500 outline-none rounded dark:bg-gray-800"
        placeholder="Begin conversation here..."
        data-testid="chat-input"
      />
      <Button
        className="px-3 py-2 sm:px-4 sm:py-2"
        type="submit"
        isLoading={generatingAnswer}
        data-testid="submit-button"
      >
        {generatingAnswer ? "Thinking..." : "Chat"}
      </Button>
      <div className="flex items-center">
        <MicButton setMessage={setMessage} />
        <ConfigModal chatId={chatId} />
      </div>
    </form>
  );
};
