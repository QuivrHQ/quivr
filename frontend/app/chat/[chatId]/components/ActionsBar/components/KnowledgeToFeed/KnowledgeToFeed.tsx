import { MdClose } from "react-icons/md";

import Button from "@/lib/components/ui/Button";

import { KnowledgeToFeedInput } from "./components/KnowledgeToFeedInput";
import { FeedItemType } from "../../types";

type FeedProps = {
  onClose: () => void;
  contents: FeedItemType[];
  addContent: (content: FeedItemType) => void;
  removeContent: (index: number) => void;
};
export const KnowledgeToFeed = ({
  onClose,
  contents,
  addContent,
  removeContent,
}: FeedProps): JSX.Element => {
  return (
    <div className="flex-col w-full relative">
      <div className="absolute right-2 top-1">
        <Button variant={"tertiary"} onClick={onClose}>
          <span>
            <MdClose className="text-3xl" />
          </span>
        </Button>
      </div>

      <KnowledgeToFeedInput
        contents={contents}
        addContent={addContent}
        removeContent={removeContent}
      />
    </div>
  );
};
