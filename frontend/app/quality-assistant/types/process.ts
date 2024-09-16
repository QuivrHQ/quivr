export interface Process {
  result: string;
  id: number;
  name: string;
  datetime: string;
  status: "pending" | "processing" | "completed" | "error";
}
