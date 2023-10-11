import { useTranslation } from "react-i18next";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import { useOnboarding } from "@/lib/hooks/useOnboarding";
import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useWelcomeChat = () => {
  const { t } = useTranslation("chat");
  const { updateOnboarding } = useOnboarding();
  const { trackOnboardingEvent } = useOnboardingTracker();

  const chat: ChatEntity = {
    chat_name: t("welcome"),
    // @ts-expect-error because we don't need to pass all the props
    chat_id: "",
  };

  const handleWelcomeChatDelete = () => {
    trackOnboardingEvent("WELCOME_CHAT_DELETED");
    void updateOnboarding({ onboarding_a: false });
  };

  return {
    chat,
    handleWelcomeChatDelete,
  };
};
