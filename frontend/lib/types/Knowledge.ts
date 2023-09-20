import { UUID } from "crypto";

export interface Knowledge {
  id: UUID;
  brain_id: UUID;
  file_name?: string;
  url?: string;
  extension: string;
  // date: Date;
}
