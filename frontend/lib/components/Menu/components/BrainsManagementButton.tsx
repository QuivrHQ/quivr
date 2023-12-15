import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";
import { LuBrain, LuChevronRight } from "react-icons/lu";

import { Button } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ActionsModal/components/Button";
import { cn } from "@/lib/utils";

export const BrainsManagementButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected =
    pathname.includes("/brains-management") && !pathname.includes("/library");
  const { t } = useTranslation("chat");

  return (
    <Link href={`/brains-management`}>
      <Button
        label={t("brains")}
        startIcon={<LuBrain />}
        endIcon={<LuChevronRight size={18} />}
        className={cn(
          "w-full hover:bg-secondary py-3 capitalize",
          isSelected ? "bg-secondary" : ""
        )}
      />
    </Link>
  );
};
