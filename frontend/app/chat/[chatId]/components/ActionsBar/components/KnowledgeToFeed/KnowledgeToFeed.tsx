import { useMemo } from "react";

import { Select } from "@/lib/components/ui/Select";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./KnowledgeToFeed.module.scss";
import { formatMinimalBrainsToSelectComponentInput } from "./utils/formatMinimalBrainsToSelectComponentInput";

export const KnowledgeToFeed = (): JSX.Element => {
  const { allBrains, setCurrentBrainId } = useBrainContext();
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
      <Select options={brainsWithUploadRights} onChange={setCurrentBrainId} />
    </div>
  );
};
