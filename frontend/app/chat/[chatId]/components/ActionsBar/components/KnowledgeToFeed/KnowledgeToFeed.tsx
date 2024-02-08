import { useMemo } from "react";

import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./KnowledgeToFeed.module.scss";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

export const KnowledgeToFeed = (): JSX.Element => {
  const { allBrains, setCurrentBrainId, currentBrain } = useBrainContext();
  const brainsWithUploadRights = formatMinimalBrainsToSelectComponentInput(
    useMemo(
      () =>
        allBrains.filter((brain) =>
          requiredRolesForUpload.includes(brain.role)
        ),
      [allBrains]
    )
  );

  return (
    <div className={styles.knowledge_to_feed_wrapper}>
      <SingleSelector
        options={brainsWithUploadRights}
        onChange={setCurrentBrainId}
        selectedOption={
          currentBrain
            ? { label: currentBrain.name, value: currentBrain.id }
            : undefined
        }
      />
    </div>
  );
};
