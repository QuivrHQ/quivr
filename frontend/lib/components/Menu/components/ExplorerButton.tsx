import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";
import { LuChevronRight, LuGlobe } from "react-icons/lu";

import { Button } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ActionsModal/components/Button";
import { cn } from "@/lib/utils";

export const ExplorerButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/library");
  const { t } = useTranslation("brain");

  return (
    <Link href={`/brains-management/library`}>
      <Button
        label={t("brain_library_button_label")}
        startIcon={<LuGlobe />}
        endIcon={<LuChevronRight size={18} />}
        className={cn(
          "font-extrabold w-full hover:bg-secondary py-3",
          isSelected ? "bg-secondary" : ""
        )}
      />
    </Link>
  );
};
