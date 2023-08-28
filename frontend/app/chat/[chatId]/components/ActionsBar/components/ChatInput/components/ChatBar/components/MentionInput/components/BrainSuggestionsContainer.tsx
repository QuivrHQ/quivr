import { Popover } from "@draft-js-plugins/mention";
import { PopoverProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Popover";

import { AddBrainModal } from "@/lib/components/AddBrainModal";

export const BrainSuggestionsContainer = ({
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
      <AddBrainModal />
    </div>
  </Popover>
);
