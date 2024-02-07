"use client";

import { useState } from "react";
import { MdLink } from "react-icons/md";

import { getFileIcon } from "@/lib/helpers/getFileIcon";
import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";

import { CrawledKnowledgeItem } from "./components/CrawledKnowledgeItem";
import { DeleteKnowledge } from "./components/DeleteKnowledge";
import { DownloadUploadedKnowledge } from "./components/DownloadUploadedKnowledge";

const KnowledgeItem = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="hover:bg-gray-50 rounded-lg flex justify-between w-full py-2 px-1"
    >
      <div className="text-sm text-gray-900 flex gap-3 items-center">
        {isUploadedKnowledge(knowledge) ? (
          getFileIcon(knowledge.fileName)
        ) : (
          <MdLink size="20" color="gray" />
        )}
        {isUploadedKnowledge(knowledge) ? (
          <p className={"max-w-[400px] truncate"}>{knowledge.fileName}</p>
        ) : (
          <CrawledKnowledgeItem url={knowledge.url} />
        )}
      </div>
      <div className="flex flex-end items-center">
        {isHovered && (
          <div className="flex items-center gap-2">
            <DownloadUploadedKnowledge knowledge={knowledge} />
            <DeleteKnowledge knowledge={knowledge} />
          </div>
        )}
      </div>
    </div>
  );
};

KnowledgeItem.displayName = "KnowledgeItem";
export default KnowledgeItem;
