interface Pricing {
  cost: number;
  description: string;
}

interface InputFile {
  key: string;
  allowed_extensions: string[];
  required: boolean;
  description: string;
}

interface InputUrl {
  key: string;
  required: boolean;
  description: string;
}

interface InputText {
  key: string;
  required: boolean;
  description: string;
  validation_regex: string;
}

interface InputBoolean {
  key: string;
  required: boolean;
  description: string;
}

interface InputNumber {
  key: string;
  required: boolean;
  description: string;
  min: number;
  max: number;
  increment: number;
  default: number;
}

interface SelectText {
  key: string;
  required: boolean;
  description: string;
  options: string[];
  default: string;
}

interface SelectNumber {
  key: string;
  required: boolean;
  description: string;
  options: number[];
  default: number;
}

interface Brain {
  required: boolean;
  description: string;
  type: string;
}

interface Inputs {
  files: InputFile[];
  urls: InputUrl[];
  texts: InputText[];
  booleans: InputBoolean[];
  numbers: InputNumber[];
  select_texts: SelectText[];
  select_numbers: SelectNumber[];
  brain: Brain;
}

export interface Assistant {
  id: number;
  name: string;
  description: string;
  pricing: Pricing;
  tags: string[];
  input_description: string;
  output_description: string;
  inputs: Inputs;
  icon_url: string;
}
