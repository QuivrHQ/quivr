import { useTranslation } from "react-i18next";
import { LuChevronRight, LuHistory } from "react-icons/lu";

import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/lib/components/ui/Popover";

import { ChatsList } from "./components/ChatsList";
import { Button } from "../Button";

export const ChatHistoryButton = (): JSX.Element => {
  const { t } = useTranslation("chat");

  return (
    <Popover>
      <PopoverTrigger className="w-full">
        <Button
          label={t("history")}
          className="w-full"
          startIcon={<LuHistory size={18} />}
          endIcon={<LuChevronRight size={18} />}
        />
      </PopoverTrigger>
      <PopoverContent
        align="center"
        className="min-h-[200px] w-[250px] max-h-[500px] overflow-auto"
      >
        <ChatsList />
      </PopoverContent>
    </Popover>
  );
};
