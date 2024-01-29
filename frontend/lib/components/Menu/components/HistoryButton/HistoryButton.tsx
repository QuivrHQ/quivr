import { useTranslation } from "react-i18next";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const HistoryButton = (): JSX.Element => {
  const { t } = useTranslation("chat");

  return (
    <MenuButton
      label={t("history")}
      isSelected={false}
      iconName="brain"
      type="open"
    />
  );
};
