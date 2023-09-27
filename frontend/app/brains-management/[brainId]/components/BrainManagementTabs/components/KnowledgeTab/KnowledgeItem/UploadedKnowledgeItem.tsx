"use client";

import { UploadedKnowledge } from "@/lib/types/Knowledge";

import { DeleteKnowledge } from "./DeleteKnowledge";
import { DownloadUploadedKnowledge } from "./DownloadUploadedKnowledge";

export const UploadedKnowledgeItem = ({
  knowledge,
}: {
  knowledge: UploadedKnowledge;
}): JSX.Element => {
  return (
    <tr key={knowledge.id}>
      <td className="px-6 py-4 whitespace-nowrap">
        <DownloadUploadedKnowledge knowledge={knowledge} />
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">
          <p className={"max-w-[400px] truncate"}>{knowledge.fileName}</p>
        </div>
      </td>
      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
        <DeleteKnowledge knowledge={knowledge} />
      </td>
    </tr>
  );
};
