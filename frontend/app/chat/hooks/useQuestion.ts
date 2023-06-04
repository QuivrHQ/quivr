import { useState } from "react";

import { useSupabase } from "@/app/supabase-provider";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useAxios } from "@/lib/useAxios";
import { redirect } from "next/navigation";
export const useQuestion = () => {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<Array<[string, string]>>([]);
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

    const response = await axiosInstance.post(`/chat/`, {
      model,
      question,
      history,
      temperature,
      max_tokens: maxTokens,
    });
    setHistory(response.data.history);
    setQuestion("");
    setIsPending(false);
  };

  return {
    isPending,
    history,
    question,
    setQuestion,
    askQuestion,
  };
};
