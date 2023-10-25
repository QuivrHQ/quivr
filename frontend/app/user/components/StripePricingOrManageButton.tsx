import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { useTranslation } from "react-i18next";

import { StripePricingModal } from "@/lib/components/Stripe";
import Button from "@/lib/components/ui/Button";
import { useUserData } from "@/lib/hooks/useUserData";

const MANAGE_PLAN_URL = process.env.NEXT_PUBLIC_STRIPE_MANAGE_PLAN_URL;

export const StripePricingOrManageButton = (): JSX.Element => {
  const { t } = useTranslation("monetization");
  const { userData } = useUserData();
  const monetizationIsOn = useFeatureIsOn("monetization");

  if (!monetizationIsOn) {
    return <></>;
  }

  const is_premium = userData?.is_premium ?? false;
  if (is_premium) {
    return (
      <a href={MANAGE_PLAN_URL} target="_blank" rel="noopener">
        <Button className="w-full">{t("manage_plan")}</Button>
      </a>
    );
  }

  return <StripePricingModal Trigger={<Button>{t("upgrade")}</Button>} />;
};
