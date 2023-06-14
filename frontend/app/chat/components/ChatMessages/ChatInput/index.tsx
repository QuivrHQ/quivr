/* eslint-disable */
"use client";
import Button from "@/lib/components/ui/Button";
import useChatsContext from "@/lib/context/ChatsProvider/hooks/useChatsContext";

import { ConfigButton } from "./ConfigButton";
import { MicButton } from "./MicButton";

export const ChatInput = (): JSX.Element => {
  const { isSendingMessage, sendMessage, setMessage, message, chat } =
    useChatsContext();

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (!isSendingMessage) {
          sendMessage(chat?.chatId);
        }
      }}
      className="sticky bottom-0 p-5 bg-white dark:bg-black rounded-t-md border border-black/10 dark:border-white/25 border-b-0 w-full max-w-3xl flex items-center justify-center gap-2 z-20"
    >
      <textarea
        autoFocus
        value={message[1]}
        onChange={(e) => setMessage((msg) => [msg[0], e.target.value])}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // Prevents the newline from being entered in the textarea
            if (!isSendingMessage) {
              sendMessage(chat?.chatId);
            } // Call the submit function here
          }
        }}
        className="w-full p-2 border border-gray-300 dark:border-gray-500 outline-none rounded dark:bg-gray-800"
        placeholder="Begin conversation here..."
      />
      <Button
        className="px-3 py-2 sm:px-4 sm:py-2"
        type="submit"
        isLoading={isSendingMessage}
      >
        {isSendingMessage ? "Thinking..." : "Chat"}
      </Button>
      <div className="flex items-center">
        <MicButton />
        <ConfigButton />
      </div>
    </form>
  );
};
