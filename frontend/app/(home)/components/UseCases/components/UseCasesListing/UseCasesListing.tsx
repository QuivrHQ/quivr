import { useEffect, useState } from "react";
import { LuPanelLeft } from "react-icons/lu";

import Spinner from "@/lib/components/ui/Spinner";
import { useDevice } from "@/lib/hooks/useDevice";
import { cn } from "@/lib/utils";

import { UseCaseComponent } from "./components/UseCaseComponent";
import { casesExamples } from "./data/cases";
import { UseCase } from "./types";

export const UseCasesListing = (): JSX.Element => {
  const [cases, setCases] = useState<UseCase[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>();
  const selectedCase = cases.find((c) => c.id === selectedCaseId);
  const { isMobile } = useDevice();

  useEffect(() => {
    setCases(casesExamples);
    setSelectedCaseId("1");
  }, []);

  if (selectedCaseId === undefined) {
    return (
      <div className="flex justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="grid grid-cols-6 md:gap-10 flex-column items-start ">
      <div className={"col-span-6 md:col-span-2 flex flex-col gap-3"}>
        {cases.map((c) => (
          <div
            key={c.id}
            onClick={() => !isMobile && setSelectedCaseId(c.id)}
            className={cn(
              "p-6 rounded-lg cursor-pointer",
              selectedCaseId === c.id &&
                "md:bg-[#7D73A7] md:border-[1px] md:border-[#6752F5]"
            )}
          >
            <h3 className="font-semibold mb-3">{c.name}</h3>
            <p>{c.description}</p>
          </div>
        ))}
      </div>

      {selectedCase !== undefined && (
        <div className="hidden md:block col-span-4 bg-white rounded-xl md:p-6 px-10 m-6">
          <LuPanelLeft className="text-black text-xl" />
          <UseCaseComponent discussions={selectedCase.discussions} />
        </div>
      )}
    </div>
  );
};
