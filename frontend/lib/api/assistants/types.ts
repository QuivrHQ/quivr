interface AssistantInput {
  key: string;
  required: boolean;
  description: string;
}

interface FilesInputAssistant extends AssistantInput {
  allowed_extensions: string[];
}

interface AssistantInputs {
  files: FilesInputAssistant[];
  urls: AssistantInput[];
  texts: AssistantInput[];
}

interface AssistantOutput {
  required: boolean;
  description: string;
  type: string;
}

interface AssistantOutputs {
  email: AssistantOutput;
  brain: AssistantOutput;
}

export interface Assistants {
  name: string;
  input_description: string;
  output_description: string;
  inputs: AssistantInputs;
  outputs: AssistantOutputs;
}
