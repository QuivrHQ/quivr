"use client";

import { AiOutlineLoading3Quarters } from "react-icons/ai";

import { KnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput";

import { useAddKnowledge } from "./hooks/useAddKnowledge";

export const AddKnowledge = (): JSX.Element => {
  const { hasPendingRequests, feedBrain } = useAddKnowledge();

  return (
    <>
      {hasPendingRequests && (
        <div className="flex mt-1 flex-col md:flex-row  shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2 md:p-6 pl-6">
          <AiOutlineLoading3Quarters className="animate-spin text-2xl md:text-3xl self-center" />
        </div>
      )}
      <div className="w-full shadow-md dark:shadow-primary/25 rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-4 mt-0 py-10">
        <KnowledgeToFeedInput feedBrain={() => void feedBrain()} />
      </div>
    </>
  );
};
