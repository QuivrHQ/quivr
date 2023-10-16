import { useEffect, useState } from "react";
import { LuPanelLeft } from "react-icons/lu";

import { useDevice } from "@/lib/hooks/useDevice";
import { cn } from "@/lib/utils";

import { Case } from "./components/Case";
import { CaseType } from "./types";

export const CasesList = (): JSX.Element => {
  const [cases, setCases] = useState<CaseType[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>();
  const selectedCase = cases.find((c) => c.id === selectedCaseId);
  const { isMobile } = useDevice();
  useEffect(() => {
    setCases([
      {
        id: "1",
        name: "Research and Studies",
        description: "Quivr is your indispensable research companion.",
        discussions: [
          {
            user: "Can you explain the ",
            quivr: `Hey there ! First you can upload documents by clicking on “+”. Then you can ask questions to your documents, and interact with them. `,
          },
          {
            user: "Cool, and what about brains ? ",
            quivr: `Brains are like your data base. You can feed a brain with multiple documents and then interact with one brain. You can also talk to Chat GPT by typing @ChatGPT4 `,
          },
        ],
      },
      {
        id: "2",
        name: "Legal research",
        description: "Your ultimate digital ally in the field of law.",
        discussions: [
          {
            user: "Can you explain the ",
            quivr: `Hey there ! First you can upload documents by clicking on “+”. Then you can ask questions to your documents, and interact with them. `,
          },
        ],
      },
      {
        id: "3",
        name: "Sales",
        description: "Placeholder",
        discussions: [
          {
            user: "Can you explain the ",
            quivr: `Hey there ! First you can upload documents by clicking on “+”. Then you can ask questions to your documents, and interact with them. `,
          },
        ],
      },
    ]);
  }, []);

  return (
    <div className="flex grid grid-cols-6 gap-10 flex flex-column items-start">
      <div
        className={cn(
          "col-span-2 flex flex-col gap-3",
          isMobile && "col-span-6"
        )}
      >
        {cases.map((c) => (
          <div
            key={c.id}
            onClick={() => !isMobile && setSelectedCaseId(c.id)}
            className={cn(
              "p-6 rounded-lg  cursor-pointer",
              selectedCaseId === c.id &&
                "bg-[#7D73A7] border-[1px] border-[#6752F5]"
            )}
          >
            <h3 className="font-semibold mb-3">{c.name}</h3>
            <p>{c.description}</p>
          </div>
        ))}
      </div>

      {selectedCase !== undefined && !isMobile && (
        <div className="col-span-4 bg-white rounded-xl p-6 px-10 m-6">
          <LuPanelLeft className="text-black text-xl" />
          <Case discussions={selectedCase.discussions} />
        </div>
      )}
    </div>
  );
};
