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
  brain_id: UUID;
  knowledge_id: UUID;
};

export const deleteKnowledge = async (
  { knowledge_id, brain_id }: DeleteKnowledgeInputProps,
  axiosInstance: AxiosInstance
): Promise<void> => {
  await axiosInstance.delete(`/knowledge/${knowledge_id}?brain_id=${brain_id}`);
};
