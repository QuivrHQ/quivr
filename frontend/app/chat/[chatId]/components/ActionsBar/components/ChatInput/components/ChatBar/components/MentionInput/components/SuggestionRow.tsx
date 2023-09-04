import { EntryComponentProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Entry/Entry";
import { useRouter } from "next/navigation";
import { MdShare } from "react-icons/md";

import { MentionTriggerType } from "@/app/chat/[chatId]/components/ActionsBar/types";
import Button from "@/lib/components/ui/Button";

import { BrainSuggestion } from "./BrainSuggestion";
import { PromptSuggestion } from "./PromptSuggestion";

export const SuggestionRow = ({
  mention,
  ...otherProps
}: EntryComponentProps): JSX.Element => {
  const router = useRouter();
  if ((mention.trigger as MentionTriggerType) === "@") {
    return (
      <div {...otherProps}>
        <div className="relative flex group px-4">
          <BrainSuggestion content={mention.name} />
          <div className="absolute right-0 flex flex-row">
            <Button
              className="group-hover:visible invisible hover:text-red-500 transition-[colors,opacity] p-1"
              onClick={() =>
                router.push(`/brains-management/${mention.id as string}#people`)
              }
              variant={"tertiary"}
              data-testId="share-brain-button"
              type="button"
            >
              <MdShare className="text-xl" />
            </Button>
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
