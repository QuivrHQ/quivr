import { useTranslation } from "react-i18next";

import { ShareModal } from "@/app/chat/components/ShareChat/ShareModal";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { ChatItemWithGroupedNotifications } from "../../types";
import { ChatItem } from "./components";
import { Onboarding } from "./components/Onboarding/Onboarding";
import { useChatDialogue } from "./hooks/useChatDialogue";
import {
  chatDialogueContainerClassName,
  chatItemContainerClassName,
} from "./styles";
import { getKeyFromChatItem } from "./utils/getKeyFromChatItem";

type MessagesDialogueProps = {
  chatItems: ChatItemWithGroupedNotifications[];
};

export const ChatDialogue = ({
  chatItems,
}: MessagesDialogueProps): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const { chatListRef } = useChatDialogue();

  const { shouldDisplayOnboardingAInstructions } = useOnboarding();

  if (shouldDisplayOnboardingAInstructions) {
    return (
      <div className={chatDialogueContainerClassName} ref={chatListRef}>
        <Onboarding />
        <div className={chatItemContainerClassName}>
          {chatItems.map((chatItem) => (
            <ChatItem key={getKeyFromChatItem(chatItem)} content={chatItem} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={chatDialogueContainerClassName} ref={chatListRef}>
      {chatItems.length === 0 ? (
        <div
          data-testid="empty-history-message"
          className="text-center opacity-50"
        >
          {t("ask", { ns: "chat" })}
        </div>
      ) : (
        <div>
          <div className="flex justify-end mb-2">
            <ShareModal />
          </div>

          <div className={chatItemContainerClassName}>
            {chatItems.map((chatItem) => (
              <ChatItem key={getKeyFromChatItem(chatItem)} content={chatItem} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
