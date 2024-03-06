import { useTranslation } from "react-i18next";

import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { ThreadItem } from "./components";
import { Onboarding } from "./components/Onboarding/Onboarding";
import { useThreadDialogue } from "./hooks/useThreadDialogue";
import {
  chatDialogueContainerClassName,
  chatItemContainerClassName,
} from "./styles";
import { getKeyFromThreadItem } from "./utils/getKeyFromThreadItem";

import { ThreadItemWithGroupedNotifications } from "../../types";

type MessagesDialogueProps = {
  chatItems: ThreadItemWithGroupedNotifications[];
};

export const ThreadDialogue = ({
  chatItems,
}: MessagesDialogueProps): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const { chatListRef } = useThreadDialogue();

  const { shouldDisplayOnboardingAInstructions } = useOnboarding();

  if (shouldDisplayOnboardingAInstructions) {
    return (
      <div className={chatDialogueContainerClassName} ref={chatListRef}>
        <Onboarding />
        <div className={chatItemContainerClassName}>
          {chatItems.map((chatItem, index) => (
            <ThreadItem
              key={getKeyFromThreadItem(chatItem)}
              content={chatItem}
              index={index}
            />
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
        <div className={chatItemContainerClassName}>
          {chatItems.map((chatItem, index) => (
            <ThreadItem
              key={getKeyFromThreadItem(chatItem)}
              content={chatItem}
              index={index}
            />
          ))}
        </div>
      )}
    </div>
  );
};
