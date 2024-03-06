import { isToday } from "date-fns";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { useThreadsContext } from "@/lib/context/ThreadsProvider/hooks/useChatsContext";

import styles from "./ThreadsButton.module.scss";
import { ThreadsSection } from "./ThreadsSection/ThreadsSection";
import { isWithinLast30Days, isWithinLast7Days, isYesterday } from "./utils";

export const ThreadsButton = (): JSX.Element => {
  const [canScrollDown, setCanScrollDown] = useState<boolean>(false);
  const { allThreads } = useThreadsContext();
  const { t } = useTranslation("thread");
  const todayThreads = allThreads.filter((chat) =>
    isToday(new Date(chat.creation_time))
  );
  const yesterdayThreads = allThreads.filter((chat) =>
    isYesterday(new Date(chat.creation_time))
  );
  const last7DaysThreads = allThreads.filter((chat) =>
    isWithinLast7Days(new Date(chat.creation_time))
  );
  const last30DaysThreads = allThreads.filter((chat) =>
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
  }, [allThreads]);

  return (
    <FoldableSection
      label={t("threads")}
      icon="history"
      foldedByDefault={true}
      hideBorder={true}
    >
      <div
        className={`
        ${styles.history_content_wrapper} 
        ${canScrollDown ? styles.fade_out : ""}
        `}
      >
        <ThreadsSection chats={todayThreads} title={t("today")} />
        <ThreadsSection chats={yesterdayThreads} title={t("yesterday")} />
        <ThreadsSection chats={last7DaysThreads} title={t("last7Days")} />
        <ThreadsSection chats={last30DaysThreads} title={t("last30Days")} />
      </div>
    </FoldableSection>
  );
};
