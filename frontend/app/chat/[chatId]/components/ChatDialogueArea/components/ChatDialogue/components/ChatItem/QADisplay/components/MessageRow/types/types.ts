import { Integration } from "@/lib/api/sync/types";

export interface SourceFile {
  filename: string;
  file_url: string;
  citations: string[];
  selected: boolean;
  integration?: Integration;
  integration_link?: string;
}
