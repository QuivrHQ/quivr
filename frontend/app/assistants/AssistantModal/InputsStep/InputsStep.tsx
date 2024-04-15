import { capitalCase } from "change-case";

import { AssistantInputs } from "@/lib/api/assistants/types";
import { FileInput } from "@/lib/components/ui/FileInput/FileInput";

interface InputsStepProps {
  inputs: AssistantInputs;
  onFileChange: (file: File, inputKey: string) => void; //
}

export const InputsStep = ({
  inputs,
  onFileChange,
}: InputsStepProps): JSX.Element => {
  return (
    <div>
      {inputs.files.map((fileInput) => (
        <FileInput
          key={fileInput.key}
          label={capitalCase(fileInput.key)}
          icon="file"
          onFileChange={(file) => onFileChange(file, fileInput.key)}
        />
      ))}
    </div>
  );
};
