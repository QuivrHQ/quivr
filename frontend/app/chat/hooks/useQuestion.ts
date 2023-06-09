import { useEffect, useState } from "react";

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

  useEffect(() => {
    // Check if history exists in local storage. If it does, fetch it and set it as history
    (async () => {
      const localHistory = localStorage.getItem("history");
      if (localHistory) {
        setHistory(JSON.parse(localHistory));
      }
    })();
  }, []);

  const askQuestion = async () => {
    setHistory((hist) => [...hist, ["user", question]]);
    setIsPending(true);

    try {
      const response = await axiosInstance.post(`/chat/`, {
        model,
        question,
        history,
        temperature,
        max_tokens: maxTokens,
      });

      setHistory(response.data.history);
      localStorage.setItem("history", JSON.stringify(response.data.history));
      setQuestion("");
    } catch (error) {
      console.error(error);
    } finally {
      setIsPending(false);
    }
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
  };
};
