import { Popover } from "@draft-js-plugins/mention";
import { PopoverProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Popover";

import { AddNewPromptButton } from "./AddNewPromptButton";

export const PromptSuggestionsContainer = ({
  children,
  ...popoverProps
}: PopoverProps): JSX.Element => (
  <Popover {...popoverProps}>
    <div
      style={{
        width: "max-content",
      }}
      className="bg-white dark:bg-black border border-black/10 dark:border-white/25 rounded-md shadow-md overflow-y-auto"
    >
      {children}
      <AddNewPromptButton />
    </div>
  </Popover>
);
