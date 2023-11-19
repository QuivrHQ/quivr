import { useTranslation } from "react-i18next";
import { PiDotsNineBold } from "react-icons/pi";


import { SidebarFooterButton } from "./SidebarFooterButton";

export const MarketPlaceButton = (): JSX.Element => {
  const { t } = useTranslation("brain");

  return (
    <SidebarFooterButton
      href={`/brains-management/library`}
      icon={<PiDotsNineBold className="w-8 h-8" />}
      label={t("brain_library_button_label")}
      data-testid="brain_library_button_label"
    />
  );
};
