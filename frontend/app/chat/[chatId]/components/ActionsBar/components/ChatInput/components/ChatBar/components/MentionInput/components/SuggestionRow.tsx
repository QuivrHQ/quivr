import { EntryComponentProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Entry/Entry";

import { BrainSuggestion } from "./BrainSuggestion";

export const SuggestionRow = ({
  mention,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  className,
  ...otherProps
}: EntryComponentProps): JSX.Element => (
  <div {...otherProps}>
    <BrainSuggestion id={mention.id as string} content={mention.name} />
  </div>
);
