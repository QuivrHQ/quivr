import { UUID } from "crypto";

export type Knowledge = UploadedKnowledge | CrawledKnowledge;

export interface UploadedKnowledge {
  id: UUID;
  brainId: UUID;
  fileName: string;
  extension: string;
}

export interface CrawledKnowledge {
  id: UUID;
  brainId: UUID;
  url: string;
  extension: string;
}

export const isUploadedKnowledge = (
  knowledge: Knowledge
): knowledge is UploadedKnowledge => {
  return "fileName" in knowledge && !("url" in knowledge);
};
