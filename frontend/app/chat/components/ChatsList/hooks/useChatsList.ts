import { useEffect } from "react";
import { useTranslation } from "react-i18next";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatsContext } from "@/lib/context/ChatsProvider/hooks/useChatsContext";
import { useToast } from "@/lib/hooks";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatsList = () => {
  const { t } = useTranslation(["chat"]);

  const { setAllChats } = useChatsContext();
  const { publish } = useToast();
  const { getChats } = useChatApi();

  useEffect(() => {
    const fetchAllChats = async () => {
      try {
        const response = await getChats();
        setAllChats(response.reverse());
      } catch (error) {
        console.error(error);
        publish({
          variant: "danger",
          text: t("errorFetching", { ns: "chat" }),
        });
      }
    };
    void fetchAllChats();
  }, []);
};
