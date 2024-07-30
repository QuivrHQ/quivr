import { UUID } from "crypto";

export type Knowledge = UploadedKnowledge | CrawledKnowledge;

export interface UploadedKnowledge {
  id: UUID;
  brainId: UUID;
  fileName: string;
  extension: string;
  status: "UPLOADED" | "PROCESSING" | "ERROR";
  integration: string;
  integration_link: string;
}

export interface CrawledKnowledge {
  id: UUID;
  brainId: UUID;
  url: string;
  extension: string;
  status: "UPLOADED" | "PROCESSING" | "ERROR";
}

export const isUploadedKnowledge = (
  knowledge: Knowledge
): knowledge is UploadedKnowledge => {
  return "fileName" in knowledge && !("url" in knowledge);
};
