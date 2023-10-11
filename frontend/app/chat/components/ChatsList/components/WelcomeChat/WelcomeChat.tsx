import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";

import { useWelcomeChat } from "./hooks/useWelcomeChat";
import { ChatsListItem } from "../ChatsListItem";

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
