import { UUID } from "crypto";

import { ShareBrain } from "@/lib/components/ShareBrain";

type BrainSuggestionProps = {
  content: string;
  id: string;
};
export const BrainSuggestion = ({
  content,
  id,
}: BrainSuggestionProps): JSX.Element => {
  return (
    <div className="relative flex group items-center">
      <div
        className={
          "flex flex-1 items-center gap-2 w-full text-left px-5 py-3 text-sm leading-5 text-gray-900 dark:text-gray-300 group-hover:bg-gray-100 dark:group-hover:bg-gray-700 group-focus:bg-gray-100 dark:group-focus:bg-gray-700 group-focus:outline-none transition-colors"
        }
      >
        <span className="flex-1">{content}</span>
      </div>
      <div className="absolute right-0 flex flex-row">
        <ShareBrain brainId={id as UUID} name={content} />
      </div>
    </div>
  );
};
