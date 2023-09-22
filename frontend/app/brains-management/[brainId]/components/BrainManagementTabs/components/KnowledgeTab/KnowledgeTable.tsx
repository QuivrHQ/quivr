import { Knowledge } from "@/lib/types/Knowledge";

import KnowledgeItem from "./KnowledgeItem";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

export const KnowledgeTable = ({
  knowledgeList,
}: KnowledgeTableProps): JSX.Element => {
  return (
    <div className="w-full">
      <table className="min-w-full divide-y divide-gray-200">
        <tbody className="bg-white divide-y divide-gray-200">
          {knowledgeList.map((knowledge) => (
            <KnowledgeItem knowledge={knowledge} key={knowledge.id} />
          ))}
        </tbody>
      </table>
    </div>
  );
};
