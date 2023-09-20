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
        <thead>
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Type
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Title
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Date
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {knowledgeList.map((knowledge) => (
            <KnowledgeItem knowledge={knowledge} key={knowledge.id} />
          ))}
        </tbody>
      </table>
    </div>
  );
};
