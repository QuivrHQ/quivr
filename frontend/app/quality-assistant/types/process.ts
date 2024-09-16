export interface Process {
  id: number;
  name: string;
  datetime: string;
  status: "pending" | "processing" | "completed" | "error";
}
