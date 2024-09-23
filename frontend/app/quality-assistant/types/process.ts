export interface Process {
  answer: string;
  id: number;
  name: string;
  creation_time: string;
  status: "pending" | "processing" | "completed" | "error";
}
