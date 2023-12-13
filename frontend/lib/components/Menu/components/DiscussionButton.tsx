import Link from "next/link";
import { usePathname } from "next/navigation";
import { LuChevronRight, LuMessageSquare } from "react-icons/lu";

import { Button } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ActionsModal/components/Button";
import { cn } from "@/lib/utils";

export const DiscussionButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/chat");

  return (
    <Link href="/chat">
      <Button
        label="Discussion"
        startIcon={<LuMessageSquare />}
        endIcon={<LuChevronRight size={18} />}
        className={cn(
          "font-extrabold w-full hover:bg-secondary py-3",
          isSelected ? "bg-secondary" : ""
        )}
      />
    </Link>
  );
};
