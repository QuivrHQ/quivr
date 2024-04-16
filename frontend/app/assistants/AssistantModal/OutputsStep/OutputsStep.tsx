import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";

import styles from "./OutputsStep.module.scss";

interface OutputsStepProps {
  setEmailOutput: (value: boolean) => void;
}

export const OutputsStep = ({
  setEmailOutput,
}: OutputsStepProps): JSX.Element => {
  return (
    <div className={styles.field_header_wrapper}>
      <Checkbox label="Checkbox" checked={false} setChecked={setEmailOutput} />
    </div>
  );
};
