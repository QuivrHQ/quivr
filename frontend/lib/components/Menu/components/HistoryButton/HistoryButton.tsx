import { isToday } from "date-fns";
import { useTranslation } from "react-i18next";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";

import { ChatsSection } from "./ChatsSection/ChatsSection";
import styles from "./HistoryButton.module.scss";
import { isWithinLast30Days, isWithinLast7Days, isYesterday } from "./utils";

export const HistoryButton = (): JSX.Element => {
  const { allChats } = useChatsContext();
  const { t } = useTranslation("chat");
  const todayChats = allChats.filter((chat) =>
    isToday(new Date(chat.creation_time))
  );
  const yesterdayChats = allChats.filter((chat) =>
    isYesterday(new Date(chat.creation_time))
  );
  const last7DaysChats = allChats.filter((chat) =>
    isWithinLast7Days(new Date(chat.creation_time))
  );
  const last30DaysChats = allChats.filter((chat) =>
    isWithinLast30Days(new Date(chat.creation_time))
  );

  return (
    <FoldableSection label={t("history")} icon="history" darkMode={true}>
      <div className={styles.history_content_wrapper}>
        <ChatsSection chats={todayChats} title={t("today")} />
        <ChatsSection chats={yesterdayChats} title={t("yesterday")} />
        <ChatsSection chats={last7DaysChats} title={t("last7Days")} />
        <ChatsSection chats={last30DaysChats} title={t("last30Days")} />
      </div>
    </FoldableSection>
  );
};
