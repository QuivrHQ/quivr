import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { CHATS_DATA_KEY } from "@/lib/api/thread/config";
import { useThreadApi } from "@/lib/api/thread/useThreadApi";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useThreadsContext } from "@/lib/context/ThreadsProvider/hooks/useChatsContext";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThreadsList = () => {
  const { t } = useTranslation(["thread"]);

  const { setAllThreads, setIsLoading } = useThreadsContext();
  const { publish } = useToast();
  const { getThreads } = useThreadApi();
  const { session } = useSupabase();

  const fetchAllThreads = async () => {
    if (session) {
      try {
        const response = await getThreads();

        return response.reverse();
      } catch (error) {
        console.error(error);
        publish({
          variant: "danger",
          text: t("errorFetching", { ns: "thread" }),
        });
      }
    }
  };

  const { data: threads, isLoading } = useQuery({
    queryKey: [CHATS_DATA_KEY],
    queryFn: fetchAllThreads,
  });

  useEffect(() => {
    setAllThreads(threads ?? []);
  }, [threads]);

  useEffect(() => {
    setIsLoading(isLoading);
  }, [isLoading]);
};
