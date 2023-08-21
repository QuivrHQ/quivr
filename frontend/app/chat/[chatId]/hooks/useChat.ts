import { AxiosError } from "axios";
import { useParams } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useChatContext } from "@/lib/context/ChatProvider/hooks/useChatContext";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import { useQuestion } from "./useQuestion";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChat = () => {
  const { track } = useEventTracking();
  const params = useParams();
  const [chatId, setChatId] = useState<string | undefined>(
    params?.chatId as string | undefined
  );
  const [generatingAnswer, setGeneratingAnswer] = useState(false);

  const { history } = useChatContext();
  const { currentBrain } = useBrainContext();
  const { publish } = useToast();
  const { createChat } = useChatApi();

  const { addStreamQuestion } = useQuestion();
  const { t } = useTranslation(["chat"]);

  const addQuestion = async (question: string, callback?: () => void) => {
    try {
      if (question === "") {
        publish({
          variant: "danger",
          text: t("ask"),
        });
        return;
      }
    } catch (error) {
      console.error({ error });

      if ((error as AxiosError).response?.status === 429) {
        publish({
          variant: "danger",
          text: t("limit_reached", { ns: "chat" }),
        });

        return;
      }

      publish({
        variant: "danger",
        text: t("error_occurred", { ns: "chat" }),
      });
    } finally {
      setGeneratingAnswer(false);
    }
  };

  return {
    history,
    addQuestion,
    generatingAnswer,
    chatId,
  };
};
