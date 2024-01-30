import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const BrainsManagementButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected =
    pathname.includes("/brains-management") && !pathname.includes("/library");
  const { t } = useTranslation("chat");

  return (
    <Link href={`/brains-management`}>
      <MenuButton
        label={t("brains")}
        isSelected={isSelected}
        iconName="brain"
        type="open"
      />
    </Link>
  );
};
