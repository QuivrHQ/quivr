import { useTranslation } from "react-i18next";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { ConnectableBrain } from "./Components/ConnectableBrain/ConnectableBrain";

export const CompositeBrainConnections = (): JSX.Element => {
  const { allBrains } = useBrainContext();
  const sortedBrains = allBrains.sort((a, b) => a.name.localeCompare(b.name));
  const { t } = useTranslation("brain");

  return (
    <div className="px-10">
      <p className="text-center mb-8 italic text-sm w-full">
        {t("composite_brain_composition_invitation")}
      </p>
      <div className="w-full flex flex-col gap-2">
        {sortedBrains.map((brain) => (
          <ConnectableBrain key={brain.id} brain={brain} />
        ))}
      </div>
    </div>
  );
};
