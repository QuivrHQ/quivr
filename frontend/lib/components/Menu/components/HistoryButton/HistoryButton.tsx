import { isToday } from "date-fns";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";

import { ChatsSection } from "./ChatsSection/ChatsSection";
import styles from "./HistoryButton.module.scss";
import { isWithinLast30Days, isWithinLast7Days, isYesterday } from "./utils";

export const HistoryButton = (): JSX.Element => {
  const [canScrollDown, setCanScrollDown] = useState<boolean>(false);
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

  useEffect(() => {
    const wrapper = document.querySelector(
      `.${styles.history_content_wrapper}`
    );

    setCanScrollDown(!!wrapper && wrapper.clientHeight >= 200);

    const handleScroll = () => {
      if (wrapper) {
        const maxScrollTop = wrapper.scrollHeight - wrapper.clientHeight;
        setCanScrollDown(
          wrapper.scrollTop < maxScrollTop && wrapper.clientHeight >= 200
        );
      }
    };

    wrapper?.addEventListener("scroll", handleScroll);

    return () => wrapper?.removeEventListener("scroll", handleScroll);
  }, [allChats]);

  return (
    <FoldableSection
      label={t("history")}
      icon="history"
      foldedByDefault={true}
      hideBorderIfUnfolded={true}
    >
      <div
        className={`
        ${styles.history_content_wrapper} 
        ${canScrollDown ? styles.fade_out : ""}
        `}
      >
        <ChatsSection chats={todayChats} title={t("today")} />
        <ChatsSection chats={yesterdayChats} title={t("yesterday")} />
        <ChatsSection chats={last7DaysChats} title={t("last7Days")} />
        <ChatsSection chats={last30DaysChats} title={t("last30Days")} />
      </div>
    </FoldableSection>
  );
};
