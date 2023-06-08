import { Dispatch, SetStateAction, useState } from "react";

import { useSupabase } from "@/app/supabase-provider";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useAxios } from "@/lib/useAxios";
import { UUID } from "crypto";
import { redirect } from "next/navigation";
import { Chat } from "../types";

interface QuestionParams {
  chatId: string | undefined;
  history?: Array<[string, string]> | undefined;
  setChats: Dispatch<SetStateAction<Chat[]>>;
}

export const useQuestion = (params: QuestionParams) => {
  const [question, setQuestion] = useState("");
  const [chatId, setChatId] = useState(params?.chatId);
  const [history, setHistory] = useState<Array<[string, string]>>(
    params?.history ?? []
  );
  const [isPending, setIsPending] = useState(false);
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();
  const {
    config: { maxTokens, model, temperature },
  } = useBrainConfig();

  if (session === null) {
    redirect("/login");
  }

  const askQuestion = async () => {
    setHistory((hist) => [...hist, ["user", question]]);
    setIsPending(true);

    const response = await axiosInstance.post<{
      chatId: UUID;
      history: Array<[string, string]>;
    }>(`/chat`, {
      ...(chatId && { chat_id: chatId }),
      model,
      question,
      history,
      temperature,
      max_tokens: maxTokens,
    });
    setHistory(response.data.history);
    localStorage.setItem("history", JSON.stringify(response.data.history));
    setQuestion("");
    setIsPending(false);

    if (chatId === undefined) {
      params.setChats((chats) => [
        ...chats,
        { chatId: response.data.chatId, history },
      ]);
    }

    setChatId(response.data.chatId);
  };

  const resetHistory = () => {
    localStorage.setItem("history", JSON.stringify([]));
    setHistory([]);
  };

  return {
    isPending,
    history,
    question,
    setQuestion,
    resetHistory,
    askQuestion,
    setChatId,
    setHistory,
  };
};
