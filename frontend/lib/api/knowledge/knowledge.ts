import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { Knowledge } from "@/lib/types/Knowledge";

export type GetAllKnowledgeInputProps = {
  brainId: UUID;
};

interface BEKnowledge {
  id: UUID;
  brain_id: UUID;
  file_name: string | null;
  url: string | null;
  extension: string;
}

export const getAllKnowledge = async (
  { brainId }: GetAllKnowledgeInputProps,
  axiosInstance: AxiosInstance
): Promise<Knowledge[]> => {
  const response = await axiosInstance.get<{
    knowledges: BEKnowledge[];
  }>(`/knowledge?brain_id=${brainId}`);

  return response.data.knowledges.map((knowledge) => {
    if (knowledge.file_name !== null) {
      return {
        id: knowledge.id,
        brainId: knowledge.brain_id,
        fileName: knowledge.file_name,
        extension: knowledge.extension,
      };
    } else if (knowledge.url !== null) {
      return {
        id: knowledge.id,
        brainId: knowledge.brain_id,
        url: knowledge.url,
        extension: "URL",
      };
    } else {
      throw new Error(`Invalid knowledge ${knowledge.id}`);
    }
  });
};

export type DeleteKnowledgeInputProps = {
  brainId: UUID;
  knowledgeId: UUID;
};

export const deleteKnowledge = async (
  { knowledgeId, brainId }: DeleteKnowledgeInputProps,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.delete(`/knowledge/${knowledgeId}?brain_id=${brainId}`);
};

export const generateSignedUrlKnowledge = async (
  { knowledgeId }: { knowledgeId: UUID },
  axiosInstance: AxiosInstance
): Promise<string> => {
  const response = await axiosInstance.get<{
    signedURL: string;
  }>(`/knowledge/${knowledgeId}/signed_download_url`);

  return response.data.signedURL;
};
