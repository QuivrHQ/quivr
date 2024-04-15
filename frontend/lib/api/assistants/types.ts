interface AssistantInput {
  key: string;
  required: boolean;
  description: string;
}

interface FilesInputAssistant extends AssistantInput {
  allowed_extensions: string[];
}

export interface AssistantInputs {
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

export interface Assistant {
  name: string;
  input_description: string;
  output_description: string;
  inputs: AssistantInputs;
  outputs: AssistantOutputs;
  tags: string[];
  icon_url: string;
  description: string;
}

export interface ProcessAssistantRequest {
  name: string;
  inputs: {
    files: {
      key: string;
      value: string;
    }[];
    urls: {
      key: string;
      value: string;
    }[];
    texts: {
      key: string;
      value: string;
    }[];
  };
  outputs: {
    email: {
      activated: boolean;
    };
    brain: {
      activated: boolean;
      value: string;
    };
  };
}
