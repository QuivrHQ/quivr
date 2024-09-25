export interface ProcessMetadata {
  input_files: string[];
}

export interface Process {
  answer: string;
  id: number;
  name: string;
  creation_time: string;
  status: "pending" | "processing" | "completed" | "error";
  assistant_name: string;
  task_metadata: ProcessMetadata;
}
