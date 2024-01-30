import { isToday } from "date-fns";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";

import styles from "./HistoryButton.module.scss";

export const HistoryButton = (): JSX.Element => {
  const { allChats } = useChatsContext();
  const { t } = useTranslation("chat");
  const todayChats = allChats.filter((chat) =>
    isToday(new Date(chat.creation_time))
  );
  //   const yesterdayChats = allChats.filter((chat) =>
  //     isYesterday(new Date(chat.creation_time))
  //   );
  //   const last7DaysChats = allChats.filter((chat) =>
  //     isWithinLast7Days(new Date(chat.creation_time))
  //   );
  //   const last30DaysChats = allChats.filter((chat) =>
  //     isWithinLast30Days(new Date(chat.creation_time))
  //   );

  return (
    <FoldableSection label={t("history")} icon="history" darkMode={true}>
      <div className={styles.history_content_wrapper}>
        {todayChats.length > 0 && (
          <div className={styles.section_title}>{t("today")}</div>
        )}
        <div className={styles.chats_wrapper}>
          {todayChats.map((chat) => (
            <Link href={`/chat/${chat.chat_id}`} key={chat.chat_id}>
              <div>{chat.chat_name.trim()}</div>
            </Link>
          ))}
        </div>
      </div>
    </FoldableSection>
  );
};
