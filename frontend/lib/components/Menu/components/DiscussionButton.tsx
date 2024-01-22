import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";
import { LuChevronRight, LuSearch } from "react-icons/lu";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton";
import { cn } from "@/lib/utils";

export const DiscussionButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/search");
  const { t } = useTranslation("chat");

  return (
    <Link href="/search">
      <MenuButton
        label={t("search")}
        startIcon={<LuSearch />}
        endIcon={<LuChevronRight size={18} />}
        className={cn(
          "w-full hover:bg-secondary py-3",
          isSelected ? "bg-secondary" : ""
        )}
      />
    </Link>
  );
};
