"use client";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionInput } from "./components";
import { MentionItem } from "./components/MentionItem";

type ChatBarProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
};

export const ChatBar = ({
  onSubmit,
  setMessage,
  message,
}: ChatBarProps): JSX.Element => {
  const { currentBrain, setCurrentBrainId, currentPrompt, setCurrentPromptId } =
    useBrainContext();

  return (
    <div className="flex flex-row flex-1 w-full item-start overflow-y-auto max-h-[10em] whitespace-pre-wrap">
      {currentBrain !== undefined && (
        <MentionItem
          text={currentBrain.name}
          onRemove={() => {
            setCurrentBrainId(null);
          }}
          trigger={"@"}
        />
      )}
      {currentPrompt !== undefined && (
        <MentionItem
          text={currentPrompt.title}
          onRemove={() => {
            setCurrentPromptId(null);
          }}
          trigger={"#"}
        />
      )}
      <div className="flex-1">
        <MentionInput
          message={message}
          setMessage={setMessage}
          onSubmit={onSubmit}
        />
      </div>
    </div>
  );
};
