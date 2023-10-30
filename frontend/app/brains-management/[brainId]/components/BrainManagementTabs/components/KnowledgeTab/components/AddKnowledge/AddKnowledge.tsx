"use client";

import { AiOutlineLoading3Quarters } from "react-icons/ai";

import { KnowledgeToFeedInput } from "@/lib/components/KnowledgeToFeedInput";

import { useAddKnowledge } from "./hooks/useAddKnowledge";

export const AddKnowledge = (): JSX.Element => {
  const {
    setShouldDisplayModal,
    shouldDisplayModal,
    hasPendingRequests,
    feedBrain,
  } = useAddKnowledge();

  return (
    <>
      <button
        className="flex flex-1 items-center justify-center rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2 md:p-6"
        onClick={() => setShouldDisplayModal(true)}
      >
        <div className="flex flex-lin items-center">
          <span className="text-2xl md:text-3xl">+</span>
        </div>
      </button>
      {hasPendingRequests && (
        <div className="flex mt-1 flex-col md:flex-row  shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2 md:p-6 pl-6">
          <AiOutlineLoading3Quarters className="animate-spin text-2xl md:text-3xl self-center" />
        </div>
      )}
      {shouldDisplayModal && (
        <KnowledgeToFeedInput feedBrain={() => void feedBrain()} />
      )}
    </>
  );
};
