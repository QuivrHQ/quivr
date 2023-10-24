import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { useTranslation } from "react-i18next";
import { FiUser } from "react-icons/fi";

import { StripePricingModal } from "@/lib/components/Stripe";
import { useUserData } from "@/lib/hooks/useUserData";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UpgradeToPlus = (): JSX.Element => {
  const { userData } = useUserData();
  const is_premium = userData?.is_premium;
  const featureIsOn = useFeatureIsOn("monetization");
  const { t } = useTranslation("monetization");

  if (!featureIsOn || is_premium === true) {
    return <></>;
  }

  return (
    <StripePricingModal
      Trigger={
        <button type="button" className={sidebarLinkStyle}>
          <FiUser className="w-8 h-8" />
          <span>
            {t("upgrade")}{" "}
            <span className="rounded bg-primary/50 py-1 px-3 text-xs">
              {t("new")}
            </span>
          </span>
        </button>
      }
    />
  );
};
