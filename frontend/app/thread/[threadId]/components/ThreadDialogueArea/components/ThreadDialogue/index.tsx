import { useTranslation } from "react-i18next";

import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { Onboarding } from "./components/Onboarding/Onboarding";
import { ThreadItem } from "./components/ThreadItem/ThreadItem";
import { useThreadDialogue } from "./hooks/useChatDialogue";
import {
  threadDialogueContainerClassName,
  threadItemContainerClassName,
} from "./styles";
import { getKeyFromThreadItem } from "./utils/getKeyFromChatItem";

import { ThreadItemWithGroupedNotifications } from "../../types";

type MessagesDialogueProps = {
  threadItems: ThreadItemWithGroupedNotifications[];
};

export const ThreadDialogue = ({
  threadItems,
}: MessagesDialogueProps): JSX.Element => {
  const { t } = useTranslation(["thread"]);
  const { threadListRef } = useThreadDialogue();

  const { shouldDisplayOnboardingAInstructions } = useOnboarding();

  if (shouldDisplayOnboardingAInstructions) {
    return (
      <div className={threadDialogueContainerClassName} ref={threadListRef}>
        <Onboarding />
        <div className={threadItemContainerClassName}>
          {threadItems.map((threadItem, index) => (
            <ThreadItem
              key={getKeyFromThreadItem(threadItem)}
              content={threadItem}
              index={index}
            />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={threadDialogueContainerClassName} ref={threadListRef}>
      {threadItems.length === 0 ? (
        <div
          data-testid="empty-history-message"
          className="text-center opacity-50"
        >
          {t("ask", { ns: "thread" })}
        </div>
      ) : (
        <div className={threadItemContainerClassName}>
          {threadItems.map((threadItem, index) => (
            <ThreadItem
              key={getKeyFromThreadItem(threadItem)}
              content={threadItem}
              index={index}
            />
          ))}
        </div>
      )}
    </div>
  );
};
