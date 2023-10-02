import Link from "next/link";
import { useTranslation } from "react-i18next";
import { FaBrain } from "react-icons/fa";

import { sidebarLinkStyle } from "@/lib/components/Sidebar/components/SidebarFooter/styles/SidebarLinkStyle";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const BrainManagementButton = (): JSX.Element => {
  const { currentBrainId } = useBrainContext();
  const { t } = useTranslation("brain");

  return (
    <Link
      href={`/brains-management/${currentBrainId ?? ""}`}
      className={sidebarLinkStyle}
      data-testid="brain-management-button"
    >
      <FaBrain className="w-8 h-8" />
      <span>{t("myBrains")}</span>
    </Link>
  );
};
