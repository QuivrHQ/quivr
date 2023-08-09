"use client";
import { useFeature } from "@growthbook/growthbook-react";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { ConfigModal } from "./components/ConfigModal";
import { MicButton } from "./components/MicButton/MicButton";
import { useChatInput } from "./hooks/useChatInput";
import { MentionItem } from "../ActionsBar/components";

export const ChatInput = (): JSX.Element => {
  const { message, setMessage, submitQuestion, chatId, generatingAnswer } =
    useChatInput();
  const { t } = useTranslation(["chat"]);
  const { currentBrain, setCurrentBrainId } = useBrainContext();
  const shouldUseNewUX = useFeature("new-ux").on;

  return (
    <form
      data-testid="chat-input-form"
      onSubmit={(e) => {
        e.preventDefault();
        submitQuestion();
      }}
      className="sticky flex items-star bottom-0 bg-white dark:bg-black w-full flex justify-center gap-2 z-20"
    >
      {currentBrain !== undefined && (
        <MentionItem
          text={currentBrain.name}
          onRemove={() => setCurrentBrainId(null)}
          prefix="@"
        />
      )}

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
        className="w-full p-2 pt-0 dark:border-gray-500 outline-none rounded dark:bg-gray-800 focus:outline-none focus:border-none"
        placeholder={
          shouldUseNewUX
            ? t("actions_bar_placeholder")
            : t("begin_conversation_placeholder")
        }
        data-testid="chat-input"
        rows={1}
      />
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
        <MicButton setMessage={setMessage} />
        <ConfigModal chatId={chatId} />
      </div>
    </form>
  );
};
