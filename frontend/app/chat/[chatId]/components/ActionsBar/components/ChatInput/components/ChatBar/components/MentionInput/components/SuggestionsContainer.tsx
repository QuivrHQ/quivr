import { Popover } from "@draft-js-plugins/mention";
import { PopoverProps } from "@draft-js-plugins/mention/lib/MentionSuggestions/Popover";

export const SuggestionsContainer = ({
  children,
  ...popoverProps
}: PopoverProps): JSX.Element => (
  <Popover {...popoverProps}>
    <div
      style={{
        maxWidth: "max-content",
      }}
      className="bg-white dark:bg-black border border-black/10 dark:border-white/25 rounded-md shadow-md overflow-y-auto"
    >
      {children}
      <button
        style={{ height: 30 }}
        onClick={() => {
          console.log("hellooo");
          alert("Hello");
        }}
      >
        Add new prompt
      </button>
    </div>
  </Popover>
);
