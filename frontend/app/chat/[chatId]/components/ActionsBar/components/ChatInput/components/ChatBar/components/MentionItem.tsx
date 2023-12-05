import { MdRemoveCircleOutline } from "react-icons/md";

import { MentionTriggerType } from "../../../../../types";

type MentionItemProps = {
  text: string;
  onRemove: () => void;
  trigger?: MentionTriggerType;
};

export const MentionItem = ({
  text,
  onRemove,
  trigger,
}: MentionItemProps): JSX.Element => {
  return (
    <div
      className="relative inline-block w-fit-content"
      data-testid="mention-item"
    >
      <div className="flex items-center bg-gray-300 mr-2 text-gray-600 rounded-2xl py-1 px-2">
        <span className="flex-grow">{`${trigger ?? ""}${text}`}</span>
        <MdRemoveCircleOutline
          className="cursor-pointer absolute top-0 right-0 mt-0 mr-0"
          data-testid="remove-mention"
          onClick={onRemove}
        />
      </div>
    </div>
  );
};
