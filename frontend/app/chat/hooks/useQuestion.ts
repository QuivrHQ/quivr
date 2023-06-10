import { Dispatch, SetStateAction, useState } from "react";

import { useSupabase } from "@/app/supabase-provider";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useAxios } from "@/lib/useAxios";
import { UUID } from "crypto";
import { redirect } from "next/navigation";
import { Chat } from "../types";

interface QuestionParams {
  chatId: string | undefined;
  setChats: Dispatch<SetStateAction<Chat[]>>;
}

export const useQuestion = (params: QuestionParams) => {
  const [question, setQuestion] = useState("");
  const [chatId, setChatId] = useState("");
  const [history, setHistory] = useState<Array<[string, string]>>([]);
  const [isPending, setIsPending] = useState(false);
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();
  const {
    config: { maxTokens, model, temperature },
  } = useBrainConfig();

  if (session === null) {
    // Declarer mes urls dans un next url -> const URL_LOGIN
    redirect("/login");
  }

  const askFirstQuestion = async () => {
    setHistory((hist) => [...hist, ["user", question]]);
    setIsPending(true);

    try {
      const response = await axiosInstance.post<{
        chatId: UUID;
        chatName: string;
        history: Array<[string, string]>;
      }>(`/chat`, {
        model,
        question,
        history,
        temperature,
        max_tokens: maxTokens,
      });
      setHistory(response.data.history);
      setQuestion("");

      params.setChats((chats) => [
        ...chats,
        {
          chatId: response.data.chatId,
          history,
          chatName: response.data.chatName,
        },
      ]);

      setChatId(response.data.chatId);
    } catch (error) {
      console.error(error);
    } finally {
      setIsPending(false);
    }
  };

  const askNextQuestion = async () => {
    setHistory((hist) => [...hist, ["user", question]]);
    setIsPending(true);
    try {
      const response = await axiosInstance.post<{
        chatId: UUID;
        history: Array<[string, string]>;
      }>(`/chat/${chatId}`, {
        model,
        question,
        history,
        temperature,
        max_tokens: maxTokens,
      });
      setHistory(response.data.history);
      setQuestion("");
    } catch (error) {
      console.error(error);
    } finally {
      setIsPending(false);
    }
  };

  return {
    isPending,
    history,
    question,
    setQuestion,
    askFirstQuestion,
    askNextQuestion,
    setHistory,
    chatId,
  };
};
