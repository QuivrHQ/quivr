"use client";

import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";

import { CrawledKnowledgeItem } from "./CrawledKnowledgeItem";
import { UploadedKnowledgeItem } from "./UploadedKnowledgeItem";

const KnowledgeItem = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  return isUploadedKnowledge(knowledge) ? (
    <UploadedKnowledgeItem knowledge={knowledge} />
  ) : (
    <CrawledKnowledgeItem knowledge={knowledge} />
  );
};

KnowledgeItem.displayName = "KnowledgeItem";
export default KnowledgeItem;
