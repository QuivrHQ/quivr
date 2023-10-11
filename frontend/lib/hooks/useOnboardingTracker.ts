import { useEventTracking } from "@/services/analytics/june/useEventTracking";

import { useOnboarding } from "./useOnboarding";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOnboardingTracker = () => {
  const { onboarding } = useOnboarding();

  const { track } = useEventTracking();

  const trackOnboardingEvent = (
    event: string,
    properties: Record<string, unknown> = {}
  ): void => {
    void track(event, {
      HOW_TO_USER_QUIVR: onboarding.onboarding_b1,
      WHAT_IS_QUIVR: onboarding.onboarding_b2,
      WHAT_IS_BRAIN: onboarding.onboarding_b3,
      ...properties,
    });
  };

  return {
    trackOnboardingEvent,
  };
};
