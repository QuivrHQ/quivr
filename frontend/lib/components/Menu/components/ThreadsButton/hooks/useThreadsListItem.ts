import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { ThreadEntity } from "@/app/thread/[threadId]/types";
import { useThreadApi } from "@/lib/api/thread/useThreadApi";
import { useThreadsContext } from "@/lib/context/ThreadsProvider/hooks/useChatsContext";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThreadsListItem = (thread: ThreadEntity) => {
  const pathname = usePathname()?.split("/").at(-1);
  const selected = thread.thread_id === pathname;
  const [threadName, setThreadName] = useState(thread.thread_name);
  const { publish } = useToast();
  const [editingName, setEditingName] = useState(false);
  const { updateThread, deleteThread } = useThreadApi();
  const { setAllThreads } = useThreadsContext();
  const router = useRouter();
  const { t } = useTranslation(["thread"]);

  const deleteThreadHandler = async () => {
    const threadId = thread.thread_id;
    try {
      await deleteThread(threadId);
      setAllThreads((threads) =>
        threads.filter((currentThread) => currentThread.thread_id !== threadId)
      );
      // TODO: Change route only when the current thread is being deleted
      void router.push("/search");
      publish({
        text: t("threadDeleted", { id: threadId, ns: "thread" }),
        variant: "success",
      });
    } catch (error) {
      console.error(t("errorDeleting", { error: error, ns: "thread" }));
      publish({
        text: t("errorDeleting", { error: error, ns: "thread" }),
        variant: "danger",
      });
    }
  };

  const updateThreadName = async () => {
    if (threadName !== thread.thread_name) {
      await updateThread(thread.thread_id, { thread_name: threadName });
      publish({
        text: t("threadNameUpdated", { ns: "thread" }),
        variant: "success",
      });
    }
  };

  const handleEditNameClick = () => {
    if (editingName) {
      setEditingName(false);
      void updateThreadName();
    } else {
      setEditingName(true);
    }
  };

  return {
    setThreadName,
    editingName,
    threadName,
    selected,
    handleEditNameClick,
    deleteThread: deleteThreadHandler,
  };
};
