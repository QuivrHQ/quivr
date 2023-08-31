"use client";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

import { ChatBar } from "./components/ChatBar/ChatBar";
import { ConfigModal } from "./components/ConfigModal";
import { useChatInput } from "./hooks/useChatInput";

export const ChatInput = (): JSX.Element => {
  const { setMessage, submitQuestion, chatId, generatingAnswer, message } =
    useChatInput();
  const { t } = useTranslation(["chat"]);

  return (
    <form
      data-testid="chat-input-form"
      onSubmit={(e) => {
        e.preventDefault();
        submitQuestion();
      }}
      className="sticky flex items-star bottom-0 bg-white dark:bg-black w-full flex justify-center gap-2 z-20"
    >
      <div className="flex flex-1 flex-col items-center">
        <ChatBar
          message={message}
          setMessage={setMessage}
          onSubmit={submitQuestion}
        />
      </div>

      <div className="flex flex-row items-end">
        <Button
          className="px-3 py-2 sm:px-4 sm:py-2"
          type="submit"
          isLoading={generatingAnswer}
          data-testid="submit-button"
        >
          {generatingAnswer
            ? t("thinking", { ns: "chat" })
            : t("chat", { ns: "chat" })}
        </Button>
        <div className="flex items-center">
          <ConfigModal chatId={chatId} />
        </div>
      </div>
    </form>
  );
};
