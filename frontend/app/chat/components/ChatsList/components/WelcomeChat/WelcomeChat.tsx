import { ChatsListItem } from "@/lib/components/ChatsListItem";
import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";

import { useWelcomeChat } from "./hooks/useWelcomeChat";

export const WelcomeChat = (): JSX.Element => {
  const { chat, handleWelcomeChatDelete } = useWelcomeChat();
  const { trackOnboardingEvent } = useOnboardingTracker();

  return (
    <div onClick={() => trackOnboardingEvent("WELCOME_CHAT_CLICKED")}>
      <ChatsListItem
        onDelete={() => void handleWelcomeChatDelete()}
        editable={false}
        chat={chat}
      />
    </div>
  );
};
