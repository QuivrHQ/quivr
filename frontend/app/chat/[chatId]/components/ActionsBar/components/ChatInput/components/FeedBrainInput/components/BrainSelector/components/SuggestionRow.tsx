import { EntryComponentProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Entry/Entry";

import { BrainSuggestion } from "./BrainSuggestion";

export const SuggestionRow = ({
  mention,
  ...otherProps
}: EntryComponentProps): JSX.Element => {
  return (
    <div {...otherProps}>
      <div className="relative flex group px-4">
        <BrainSuggestion content={mention.name} />
      </div>
    </div>
  );
};
