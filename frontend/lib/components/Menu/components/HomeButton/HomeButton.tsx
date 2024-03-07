import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const HomeButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/search");
  const { t } = useTranslation("chat");

  return (
    <Link href={`/search`}>
      <MenuButton
        label={t("home")}
        isSelected={isSelected}
        iconName="home"
        type="open"
        color="primary"
      />
    </Link>
  );
};
