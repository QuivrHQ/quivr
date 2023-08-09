import { useParams } from "next/navigation";
import { useEffect } from "react";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatContext } from "@/lib/context";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSelectedChatPage = () => {
  const { setHistory } = useChatContext();
  const { getHistory } = useChatApi();

  const params = useParams();
  const chatId = params?.chatId as string | undefined;

  useEffect(() => {
    const fetchHistory = async () => {
      if (chatId === undefined) {
        setHistory([]);

        return;
      }

      const chatHistory = await getHistory(chatId);

      if (chatHistory.length > 0) {
        setHistory(chatHistory);
      }
    };
    void fetchHistory();
  }, [chatId, setHistory]);
};
