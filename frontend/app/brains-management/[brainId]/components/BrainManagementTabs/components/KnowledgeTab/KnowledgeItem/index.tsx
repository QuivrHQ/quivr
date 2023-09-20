"use client";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { Knowledge } from "@/lib/types/Knowledge";

import { useKnowledgeItem } from "./useKnowledgeItem";

const KnowledgeItem = ({
  knowledge,
}: {
  knowledge: Knowledge;
}): JSX.Element => {
  const { isDeleting, onDeleteKnowledge } = useKnowledgeItem();

  const { currentBrain } = useBrainContext();

  const canDeleteFile = currentBrain?.role === "Owner";

  console.log("isDeleting", isDeleting);

  const knowledge_name = knowledge.file_name ?? knowledge.url;

  // TODO: Add the two types to avoid this. Knowledge = UploadedKnowledge | CrawledKnowledge
  if (knowledge_name === undefined) {
    return <></>;
  }

  return (
    <tr key={knowledge.id}>
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="flex items-center">
          {/* Display the icon for the type (e.g., PDF, Excel) here */}
          <span className="text-sm font-medium text-gray-900">
            {knowledge.extension}
          </span>
        </div>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">
          <p className={"max-w-[400px] truncate"}>{knowledge_name}</p>
        </div>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">Toto</div>
      </td>
      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
        {/* <button
            className="text-indigo-600 hover:text-indigo-900 mr-4"
            onClick={() => onDownload(knowledge.id)}
          >
            Download
          </button> */}
        {canDeleteFile && (
          <button
            className="text-red-600 hover:text-red-900"
            onClick={() => void onDeleteKnowledge(knowledge)}
          >
            Delete
          </button>
        )}
      </td>
    </tr>
  );
};

KnowledgeItem.displayName = "KnowledgeItem";
export default KnowledgeItem;
