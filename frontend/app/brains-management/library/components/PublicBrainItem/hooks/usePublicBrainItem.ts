import { UUID } from "crypto";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useSubscriptionApi } from "@/lib/api/subscription/useSubscriptionApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { getAxiosErrorParams } from "@/lib/helpers/getAxiosErrorParams";
import { useToast } from "@/lib/hooks";

type UseSubscribeToBrainProps = {
  brainId: UUID;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePublicBrainItem = ({ brainId }: UseSubscribeToBrainProps) => {
  const { subscribeToBrain } = useSubscriptionApi();
  const [subscriptionRequestPending, setSubscriptionRequestPending] =
    useState(false);
  const { publish } = useToast();
  const { allBrains, fetchAllBrains } = useBrainContext();

  const [isSubscriptionModalOpened, setIsSubscriptionModalOpened] =
    useState(false);

  const isUserSubscribedToBrain =
    allBrains.find((brain) => brain.id === brainId) !== undefined;

  const { t } = useTranslation("brain");
  const handleSubscribeToBrain = async () => {
    try {
      setSubscriptionRequestPending(true);

      await subscribeToBrain(brainId);
      setIsSubscriptionModalOpened(false);
      await fetchAllBrains();
      publish({
        text: t("public_brain_subscription_success_message"),
        variant: "success",
      });
    } catch (e) {
      const error = getAxiosErrorParams(e);
      if (error !== undefined) {
        publish({
          text: error.message,
          variant: "danger",
        });

        return;
      }
      publish({
        text: JSON.stringify(error),
        variant: "danger",
      });
    } finally {
      setSubscriptionRequestPending(false);
    }
  };

  return {
    handleSubscribeToBrain,
    subscriptionRequestPending,
    isUserSubscribedToBrain,
    setIsSubscriptionModalOpened,
    isSubscriptionModalOpened,
  };
};
