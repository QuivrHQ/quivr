import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const BrainsManagementButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected =
    pathname.includes("/brains-management") && !pathname.includes("/library");
  const { t } = useTranslation("brain");

  return (
    <Link href={`/brains-management`}>
      <MenuButton
        label={t("manage_brains")}
        isSelected={isSelected}
        iconName="brainCircuit"
        type="open"
        color="primary"
      />
    </Link>
  );
};
