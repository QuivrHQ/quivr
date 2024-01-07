import { useSearchParams } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useSubscriptionApi } from "@/lib/api/subscription/useSubscriptionApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { PublicBrain } from "@/lib/context/BrainProvider/types";
import { getAxiosErrorParams } from "@/lib/helpers/getAxiosErrorParams";
import { useToast } from "@/lib/hooks";

import { generatePublicBrainLink } from "../utils/generatePublicBrainLink";

type UseSubscribeToBrainProps = {
  brain: PublicBrain;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePublicBrainItem = ({ brain }: UseSubscribeToBrainProps) => {
  const brainId = brain.id;

  const { subscribeToBrain } = useSubscriptionApi();
  const [subscriptionRequestPending, setSubscriptionRequestPending] =
    useState(false);
  const { publish } = useToast();
  const { allBrains, fetchAllBrains } = useBrainContext();
  const { register, watch } = useForm<{
    secrets?: Record<string, string>;
  }>({});
  const secrets = watch("secrets") ?? {};

  const searchParams = useSearchParams();
  const urlBrainId = searchParams?.get("brainId");

  const [isSubscriptionModalOpened, setIsSubscriptionModalOpened] = useState(
    urlBrainId === brainId
  );

  const isUserSubscribedToBrain =
    allBrains.find((_brain) => _brain.id === brainId) !== undefined;

  const { t } = useTranslation("brain");

  const subscribeUserToBrain = async () => {
    try {
      setSubscriptionRequestPending(true);

      await subscribeToBrain(brainId, secrets);
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
  const handleBrainSubscription = () => {
    const brainHasSecretsLength = brain.brain_definition?.secrets?.length ?? 0;

    if (brain.brain_type === "api") {
      const filledSecretsLength = Object.keys(secrets).filter(
        (key) => secrets[key].length > 0
      ).length;
      if (
        brainHasSecretsLength > 0 &&
        filledSecretsLength !== brainHasSecretsLength
      ) {
        setIsSubscriptionModalOpened(true);

        return;
      }
    }

    void subscribeUserToBrain();
  };

  return {
    subscriptionRequestPending,
    isUserSubscribedToBrain,
    setIsSubscriptionModalOpened,
    isSubscriptionModalOpened,
    handleCopyBrainLink,
    handleBrainSubscription,
    register,
  };
};
