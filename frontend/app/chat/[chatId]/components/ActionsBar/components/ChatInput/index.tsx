"use client";
import { useTranslation } from "react-i18next";
import { MdAddCircle, MdSend } from "react-icons/md";

import Button from "@/lib/components/ui/Button";

import { ChatBar } from "./components/ChatBar/ChatBar";
import { ConfigModal } from "./components/ConfigModal";
import { FeedBrainInput } from "./components/FeedBrainInput";
import { useChatInput } from "./hooks/useChatInput";

export const ChatInput = (): JSX.Element => {
  const {
    setMessage,
    submitQuestion,
    chatId,
    generatingAnswer,
    message,
    isUploading,
    setIsUploading,
  } = useChatInput();
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
      <div className="flex items-start">
        <Button
          className="p-0"
          variant={"tertiary"}
          data-testid="upload-button"
          type="button"
          onClick={() => setIsUploading(true)}
        >
          <MdAddCircle className="text-3xl" />
        </Button>
      </div>

      <div className="flex flex-1 flex-col items-center">
        {isUploading ? (
          <FeedBrainInput />
        ) : (
          <ChatBar
            message={message}
            setMessage={setMessage}
            onSubmit={submitQuestion}
          />
        )}
      </div>

      <div className="flex flex-row items-end">
        {isUploading ? (
          <div className="flex items-center">
            <Button variant="tertiary" onClick={() => setIsUploading(false)}>
              {/* rotate the icon to 90° */}
              <MdSend
                className="text-3xl 
              transform rotate-270
              "
              />
            </Button>
          </div>
        ) : (
          <>
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
          </>
        )}
      </div>
    </form>
  );
};
