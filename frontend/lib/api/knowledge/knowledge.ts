import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import {
  AddFolderData,
  AddKnowledgeFileData,
  AddKnowledgeUrlData,
} from "@/lib/types/Knowledge";

import { KMSElement } from "../sync/types";

export type GetAllKnowledgeInputProps = {
  brainId: UUID;
};

interface BEKnowledge {
  id: UUID;
  brain_id: UUID;
  file_name: string | null;
  url: string | null;
  extension: string;
  status: string;
  integration: string;
  integration_link: string;
}

export const getAllBrainKnowledge = async (
  { brainId }: GetAllKnowledgeInputProps,
  axiosInstance: AxiosInstance
): Promise<KMSElement[]> => {
  const response = await axiosInstance.get<{
    knowledges: KMSElement[];
  }>(`/knowledge?brain_id=${brainId}`);

  return response.data.knowledges;
};

export type DeleteKnowledgeInputProps = {
  brainId?: UUID;
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

export const getFiles = async (
  parentId: UUID | null,
  axiosInstance: AxiosInstance
): Promise<KMSElement[]> => {
  return (
    await axiosInstance.get<KMSElement[]>(`/knowledge/files`, {
      params: { parent_id: parentId },
    })
  ).data;
};

export const addFolder = async (
  knowledgeData: AddFolderData,
  axiosInstance: AxiosInstance
): Promise<BEKnowledge> => {
  const formData = new FormData();
  formData.append("knowledge_data", JSON.stringify(knowledgeData));
  formData.append("file", "");

  return (
    await axiosInstance.post<BEKnowledge>(`/knowledge/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
  ).data;
};

export const addKnowledgeFile = async (
  knowledgeData: AddKnowledgeFileData,
  file: File,
  axiosInstance: AxiosInstance
): Promise<BEKnowledge> => {
  const formData = new FormData();
  formData.append("knowledge_data", JSON.stringify(knowledgeData));
  formData.append("file", file);

  return (
    await axiosInstance.post<BEKnowledge>(`/knowledge/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
  ).data;
};

export const addKnowledgeUrl = async (
  knowledgeData: AddKnowledgeUrlData,
  axiosInstance: AxiosInstance
): Promise<BEKnowledge> => {
  const formData = new FormData();
  formData.append("knowledge_data", JSON.stringify(knowledgeData));

  return (
    await axiosInstance.post<BEKnowledge>(`/knowledge/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
  ).data;
};

export const patchKnowledge = async (
  knowledge_id: UUID,
  axiosInstance: AxiosInstance,
  parent_id: UUID | null
): Promise<KMSElement> => {
  const data = {
    parent_id,
  };

  const response: { data: KMSElement } = await axiosInstance.patch<KMSElement>(
    `/knowledge/${knowledge_id}`,
    data
  );

  return response.data;
};

export const linkKnowledgeToBrains = async (
  knowledge: KMSElement,
  brainIds: UUID[],
  axiosInstance: AxiosInstance
): Promise<KMSElement[]> => {
  const response = await axiosInstance.post<KMSElement[]>(
    `/knowledge/link_to_brains/`,
    {
      knowledge,
      brain_ids: brainIds,
    }
  );

  return response.data;
};

export const unlinkKnowledgeFromBrains = async (
  knowledge_id: UUID,
  brainIds: UUID[],
  axiosInstance: AxiosInstance
): Promise<KMSElement[]> => {
  const response = await axiosInstance.delete<KMSElement[]>(
    `/knowledge/unlink_from_brains/`,
    {
      data: {
        knowledge_id,
        brain_ids: brainIds,
      },
    }
  );

  return response.data;
};
