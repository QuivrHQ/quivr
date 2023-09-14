"use client";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainSelector } from "./components";
import { useFeedBrainInput } from "./hooks/useFeedBrainInput";
import { MentionItem } from "../ChatBar/components/MentionItem";

type FeedBrainInputProps = {
  onSubmit: () => void;
};

export const FeedBrainInput = ({
  onSubmit,
}: FeedBrainInputProps): JSX.Element => {
  const { currentBrain, setCurrentBrainId } = useBrainContext();

  useFeedBrainInput();

  return (
    <div className="mt-3 flex flex-row flex-1 w-full item-start">
      {currentBrain !== undefined && (
        <MentionItem
          text={currentBrain.name}
          onRemove={() => {
            setCurrentBrainId(null);
          }}
          trigger={"@"}
        />
      )}
      <div className="flex-1">
        <BrainSelector onSubmit={onSubmit} />
      </div>
    </div>
  );
};
