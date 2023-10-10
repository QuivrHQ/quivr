import { useTranslation } from "react-i18next";

import { ChatEntity } from "@/app/chat/[chatId]/types";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { ChatsListItem } from "./ChatsListItem";

export const WelcomeChat = (): JSX.Element => {
  const { t } = useTranslation("chat");
  const chat: ChatEntity = {
    chat_name: t("welcome"),
    // @ts-expect-error because we don't need to pass all the props
    chat_id: "",
  };
  const { updateOnboarding } = useOnboarding();

  return (
    <ChatsListItem
      onDelete={() => void updateOnboarding({ onboarding_a: false })}
      editable={false}
      chat={chat}
    />
  );
};
