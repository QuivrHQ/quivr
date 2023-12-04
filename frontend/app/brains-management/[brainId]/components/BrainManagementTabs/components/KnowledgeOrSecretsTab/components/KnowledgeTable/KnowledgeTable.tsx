import { Knowledge } from "@/lib/types/Knowledge";

import KnowledgeItem from "./components/KnowledgeItem";

interface KnowledgeTableProps {
  knowledgeList: Knowledge[];
}

export const KnowledgeTable = ({
  knowledgeList,
}: KnowledgeTableProps): JSX.Element => {
  return (
    <div className="w-full shadow-md dark:shadow-primary/25 rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 mt-0 p-5">
      {knowledgeList.map((knowledge) => (
        <KnowledgeItem knowledge={knowledge} key={knowledge.id} />
      ))}
    </div>
  );
};
