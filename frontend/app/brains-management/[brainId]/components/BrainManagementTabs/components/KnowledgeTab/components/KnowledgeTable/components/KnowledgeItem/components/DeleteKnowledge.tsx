"use client";

import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { MdDelete } from "react-icons/md";

import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";
import { Knowledge } from "@/lib/types/Knowledge";

import { useKnowledgeItem } from "../hooks/useKnowledgeItem";

export const DeleteKnowledge = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  const { isDeleting, onDeleteKnowledge } = useKnowledgeItem();
  const { brain } = useUrlBrain();

  const canDeleteFile = brain?.role === "Owner";

  if (!canDeleteFile) {
    return <></>;
  }

  return isDeleting ? (
    <AiOutlineLoading3Quarters />
  ) : (
    <button onClick={() => void onDeleteKnowledge(knowledge)}>
      <MdDelete size="20" />
    </button>
  );
};
