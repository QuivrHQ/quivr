import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { Knowledge } from "@/lib/types/Knowledge";

export type GetAllKnowledgeInputProps = {
  brainId: UUID;
};

export const getAllKnowledge = async (
  { brainId }: GetAllKnowledgeInputProps,
  axiosInstance: AxiosInstance
): Promise<Knowledge[]> => {
  const response = await axiosInstance.get<{
    knowledges: Knowledge[];
  }>(`/knowledge?brain_id=${brainId}`);

  console.log("response.data", response.data);

  return response.data.knowledges;
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
