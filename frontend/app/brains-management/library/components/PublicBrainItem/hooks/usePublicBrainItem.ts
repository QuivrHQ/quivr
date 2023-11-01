import { UUID } from "crypto";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useSubscriptionApi } from "@/lib/api/subscription/useSubscriptionApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { getAxiosErrorParams } from "@/lib/helpers/getAxiosErrorParams";
import { useToast } from "@/lib/hooks";

import { generatePublicBrainLink } from "../utils/generatePublicBrainLink";

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

  const searchParams = useSearchParams();
  const urlBrainId = searchParams?.get("brainId");

  const [isSubscriptionModalOpened, setIsSubscriptionModalOpened] = useState(
    urlBrainId === brainId
  );

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

  const handleCopyBrainLink = async () => {
    await navigator.clipboard.writeText(generatePublicBrainLink(brainId));
    publish({
      variant: "success",
      text: t("copiedToClipboard", { ns: "brain" }),
    });
  };

  return {
    handleSubscribeToBrain,
    subscriptionRequestPending,
    isUserSubscribedToBrain,
    setIsSubscriptionModalOpened,
    isSubscriptionModalOpened,
    handleCopyBrainLink,
  };
};
