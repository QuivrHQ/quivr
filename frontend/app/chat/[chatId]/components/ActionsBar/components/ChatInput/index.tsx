/* eslint-disable */
"use client";
import { useTranslation } from "react-i18next";
import { MdAddCircle, MdSend } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { ChatBar } from "./components/ChatBar/ChatBar";
import { ConfigModal } from "./components/ConfigModal";
import { FeedBrainInput } from "./components/FeedBrainInput";
import { useChatInput } from "./hooks/useChatInput";

type ChatInputProps = {
  shouldDisplayUploadCard: boolean;
  feedBrain: () => void;
  setShouldDisplayUploadCard: (shouldDisplayUploadCard: boolean) => void;
  hasContentToFeedBrain: boolean;
};

export const ChatInput = ({
  shouldDisplayUploadCard,
  feedBrain,
  setShouldDisplayUploadCard,
  hasContentToFeedBrain,
}: ChatInputProps): JSX.Element => {
  const { setMessage, submitQuestion, chatId, generatingAnswer, message } = useChatInput();
  const { t } = useTranslation(["chat"]);
  const { currentBrainId } = useBrainContext();

  const isEmptyMessage = !message || message.trim() === '';

  return (
    <form
      data-testid="chat-input-form"
      onSubmit={(e) => {
        e.preventDefault();
        submitQuestion();
      }}
      className="sticky bottom-0 bg-white dark:bg-black w-full flex items-center gap-2 z-20 p-2"
    >
      {!shouldDisplayUploadCard && (
        <Button
          className="p-0"
          variant={"tertiary"}
          data-testid="upload-button"
          type="button"
          onClick={() => setShouldDisplayUploadCard(true)}
        >
          <MdAddCircle className="text-3xl" />
        </Button>
      )}

      <div className="flex flex-1 flex-col items-center">
        {shouldDisplayUploadCard ? (
          <FeedBrainInput onSubmit={feedBrain} />
        ) : (
          <ChatBar
            message={message}
            setMessage={setMessage}
            onSubmit={submitQuestion}
          />
        )}
      </div>

      <div className="flex flex-row items-end">
        {shouldDisplayUploadCard ? (
          <Button
            disabled={currentBrainId === null || !hasContentToFeedBrain}
            variant="tertiary"
            onClick={feedBrain}
            type="button"
          >
            <MdSend className="text-3xl transform -rotate-90" />
          </Button>
        ) : (
          <>
            {isEmptyMessage ? (
              <div className="md:hidden flex items-center">
                <ConfigModal chatId={chatId} />
              </div>
            ) : (
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
            )}
            <div className="hidden md:flex items-center">
              <ConfigModal chatId={chatId} />
            </div>
          </>
        )}
      </div>
    </form>
  );
};