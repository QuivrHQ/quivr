import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";

import { ONBOARDING_DATA_KEY } from "@/lib/api/onboarding/config";
import { useOnboardingApi } from "@/lib/api/onboarding/useOnboardingApi";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOnboarding = () => {
  const shouldDisplayOnboarding = useFeatureIsOn("onboarding");
  const { getOnboarding } = useOnboardingApi();
  const params = useParams();

  const chatId = params?.chatId as string | undefined;

  const { data: onboarding } = useQuery({
    queryFn: getOnboarding,
    queryKey: [ONBOARDING_DATA_KEY],
  });

  const shouldDisplayOnboardingA =
    shouldDisplayOnboarding &&
    chatId === undefined &&
    onboarding?.onboarding_a === true;

  return {
    onboarding,
    shouldDisplayOnboardingA,
  };
};
