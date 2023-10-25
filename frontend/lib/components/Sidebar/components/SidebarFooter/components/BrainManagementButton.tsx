import { useTranslation } from "react-i18next";
import { FaBrain } from "react-icons/fa";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { SidebarFooterButton } from "./SidebarFooterButton";

export const BrainManagementButton = (): JSX.Element => {
  const { currentBrainId } = useBrainContext();
  const { t } = useTranslation("brain");

  return (
    <SidebarFooterButton
      href={`/brains-management/${currentBrainId ?? ""}`}
      icon={<FaBrain className="w-8 h-8" />}
      label={t("myBrains")}
      data-testid="brain-management-button"
    />
  );
};
