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
    <div className="relative inline-block w-fit-content">
      <div className="flex items-center bg-gray-300 mr-2 text-gray-600 rounded-2xl py-1 px-2">
        <span className="flex-grow">{`${trigger ?? ""}${text}`}</span>
        <MdRemoveCircleOutline
          className="cursor-pointer absolute top-[-10px] right-[5px]"
          onClick={onRemove}
        />
      </div>
    </div>
  );
};
