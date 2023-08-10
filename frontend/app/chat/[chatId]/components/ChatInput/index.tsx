"use client";
import { useFeature } from "@growthbook/growthbook-react";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { ChatBar } from "./components/ChatInputV2/ChatBar";
import { ConfigurationProvider } from "./components/ChatInputV2/ConfigurationProvider";
import { ConfigModal } from "./components/ConfigModal";
import { MicButton } from "./components/MicButton/MicButton";
import { useChatInput } from "./hooks/useChatInput";

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
      <div className="flex flex-col items-center">
        <ConfigurationProvider>
          <ChatBar />
        </ConfigurationProvider>
      </div>

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
