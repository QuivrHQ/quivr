import { PopoverAnchor } from "@radix-ui/react-popover";
import { useState } from "react";
import { LuPlusCircle, LuXCircle } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/lib/components/ui/Popover";

import { ChangeBrainButton } from "./components/ChangeBrainButton";
import { ChatHistoryButton } from "./components/ChatHistoryButton/ChatHistoryButton";
import { ConfigModal } from "./components/ConfigModal";
import { FeedCardTrigger } from "./components/FeedCardTrigger";
import { NewDiscussionButton } from "./components/NewDiscussionButton";
import { SelectedBrainTag } from "./components/SelectedBrainTag";

export const ActionsModal = (): JSX.Element => {
  const [isActionsModalOpened, setIsActionsModalOpened] = useState(false);

  const Icon = isActionsModalOpened ? LuXCircle : LuPlusCircle;

  return (
    <div className="flex items-center">
      <Popover
        open={isActionsModalOpened}
        onOpenChange={(isOpened) => setIsActionsModalOpened(isOpened)}
      >
        <PopoverTrigger>
          <PopoverAnchor asChild>
            <Button variant="tertiary" type="button" className="p-0">
              <Icon className="text-accent font-bold" size={30} />
            </Button>
          </PopoverAnchor>
        </PopoverTrigger>
        <PopoverContent
          align="end"
          sideOffset={15}
          className="min-h-[200px] w-[250px]"
        >
          <SelectedBrainTag />
          <NewDiscussionButton />
          <FeedCardTrigger />
          <ChatHistoryButton />
          <ConfigModal />
          <ChangeBrainButton />
        </PopoverContent>
      </Popover>
    </div>
  );
};
