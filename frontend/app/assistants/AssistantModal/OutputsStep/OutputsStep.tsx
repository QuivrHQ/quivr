import { useMemo, useState } from "react";

import { formatMinimalBrainsToSelectComponentInput } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/utils/formatMinimalBrainsToSelectComponentInput";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { requiredRolesForUpload } from "@/lib/config/upload";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./OutputsStep.module.scss";

interface OutputsStepProps {
  setEmailOutput: (value: boolean) => void;
  setBrainOutput: (value: string) => void;
}

export const OutputsStep = ({
  setEmailOutput,
  setBrainOutput,
}: OutputsStepProps): JSX.Element => {
  const [existingBrainChecked, setExistingBrainChecked] =
    useState<boolean>(false);
  const [selectedBrainId, setSelectedBrainId] = useState<string>("");
  const { allBrains } = useBrainContext();

  const brainsWithUploadRights = formatMinimalBrainsToSelectComponentInput(
    useMemo(
      () =>
        allBrains.filter(
          (brain) =>
            requiredRolesForUpload.includes(brain.role) && !!brain.max_files
        ),
      [allBrains]
    )
  );

  return (
    <div className={styles.outputs_wrapper}>
      <MessageInfoBox type="info">
        It can take a few minutes to process.
      </MessageInfoBox>
      <Checkbox
        label="Receive the results by Email"
        checked={true}
        setChecked={setEmailOutput}
      />
      <Checkbox
        label="Upload the results on an existing Brain"
        checked={existingBrainChecked}
        setChecked={() => {
          if (existingBrainChecked) {
            setBrainOutput("");
            setSelectedBrainId("");
          }
          setExistingBrainChecked(!existingBrainChecked);
        }}
      />
      {existingBrainChecked && (
        <div className={styles.brain_selector}>
          <SingleSelector
            options={brainsWithUploadRights}
            onChange={(brain) => {
              setBrainOutput(brain);
              setSelectedBrainId(brain);
            }}
            selectedOption={
              selectedBrainId
                ? {
                    value: selectedBrainId,
                    label: allBrains.find(
                      (brain) => brain.id === selectedBrainId
                    )?.name as string,
                  }
                : undefined
            }
            placeholder="Select a brain"
            iconName="brain"
          />
        </div>
      )}
    </div>
  );
};
