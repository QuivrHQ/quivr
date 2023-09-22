"use client";

import { MdLink } from "react-icons/md";

import { CrawledKnowledge } from "@/lib/types/Knowledge";

import { DeleteKnowledge } from "./DeleteKnowledge";

export const CrawledKnowledgeItem = ({
  knowledge,
}: {
  knowledge: CrawledKnowledge;
}): JSX.Element => {
  return (
    <tr key={knowledge.id}>
      <td className="px-6 py-4 whitespace-nowrap">
        <a href={knowledge.url} target="_blank" rel="noopener noreferrer">
          <MdLink size="20" color="gray" />
        </a>
      </td>
      <td className="px-6 py-4 whitespace-nowrap">
        <div className="text-sm text-gray-900">
          <p className={"max-w-[400px] truncate"}>{knowledge.url}</p>
        </div>
      </td>
      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
        <DeleteKnowledge knowledge={knowledge} />
      </td>
    </tr>
  );
};
