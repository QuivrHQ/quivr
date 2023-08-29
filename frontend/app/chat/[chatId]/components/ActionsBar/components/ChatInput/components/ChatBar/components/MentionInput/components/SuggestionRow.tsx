import { EntryComponentProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Entry/Entry";
import { UUID } from "crypto";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";
import { ShareBrain } from "@/lib/components/ShareBrain";

import { BrainSuggestion } from "./BrainSuggestion";
import { PromptSuggestion } from "./PromptSuggestion";

export const SuggestionRow = ({
  mention,
  ...otherProps
}: EntryComponentProps): JSX.Element => {
  if ((mention.trigger as MentionTriggerType) === "@") {
    return (
      <div {...otherProps}>
        <div className="relative flex group px-4">
          <BrainSuggestion content={mention.name} />
          <div className="absolute right-0 flex flex-row">
            <ShareBrain brainId={mention.id as UUID} />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div {...otherProps}>
      <PromptSuggestion content={mention.name} />
    </div>
  );
};
