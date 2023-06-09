"use client";
import { UUID } from "crypto";
import Button from "../../../../components/ui/Button";
import useChats from "../../../hooks/useChats";
import { ConfigButton } from "./ConfigButton";
import { MicButton } from "./MicButton";

export function ChatInput({ chatId }: { chatId?: UUID }) {
  const { isSendingMessage, sendMessage, setMessage, message } = useChats();
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (!isSendingMessage) sendMessage(chatId);
      }}
      className="sticky bottom-0 w-full flex items-center justify-center gap-2"
    >
      <textarea
        autoFocus
        value={message[1]}
        onChange={(e) => setMessage((msg) => [msg[0], e.target.value])}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // Prevents the newline from being entered in the textarea
            if (!isSendingMessage) sendMessage(chatId); // Call the submit function here
          }
        }}
        className="w-full p-2 border border-gray-300 dark:border-gray-500 outline-none rounded dark:bg-gray-800"
        placeholder="Begin conversation here..."
      />
      <Button type="submit" isLoading={isSendingMessage}>
        {isSendingMessage ? "Thinking..." : "Chat"}
      </Button>
      <MicButton />
      <ConfigButton />
    </form>
  );
}
