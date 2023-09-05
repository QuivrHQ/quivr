"use client";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainSelector } from "./components";
import { useFeedBrainInput } from "./hooks/useFeedBrainInput";
import { MentionItem } from "../ChatBar/components/MentionItem";

export const FeedBrainInput = (): JSX.Element => {
  const { currentBrain, setCurrentBrainId } = useBrainContext();

  useFeedBrainInput();

  return (
    <div className="flex flex-row flex-1 w-full item-start">
      <div className="flex-1">
        <div className="mt-3">
          {currentBrain !== undefined && (
            <MentionItem
              text={currentBrain.name}
              onRemove={() => {
                setCurrentBrainId(null);
              }}
              trigger={"@"}
            />
          )}
          <BrainSelector />
        </div>
      </div>
    </div>
  );
};
