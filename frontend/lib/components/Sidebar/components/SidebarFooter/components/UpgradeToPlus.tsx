import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { useTranslation } from "react-i18next";
import { FiUser } from "react-icons/fi";

import { StripePricingModal } from "@/lib/components/Stripe";
import { useUserData } from "@/lib/hooks/useUserData";

import { SidebarFooterButton } from "./SidebarFooterButton";

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
        <SidebarFooterButton
          icon={<FiUser className="w-8 h-8" />}
          label={
            <div className="flex justify-between items-center w-full">
              {t("upgrade")}
              <span className="rounded bg-primary/30 py-1 px-3 text-xs">
                {t("new")}
              </span>
            </div>
          }
        />
      }
    />
  );
};
