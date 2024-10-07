import { UUID } from "crypto";

import { useAxios } from "@/lib/hooks";
import { AddFolderData } from "@/lib/types/Knowledge";

import { KMSElement } from "../sync/types";
import {
  addFolder,
  deleteKnowledge,
  DeleteKnowledgeInputProps,
  generateSignedUrlKnowledge,
  getAllBrainKnowledge,
  GetAllKnowledgeInputProps,
  getFiles,
  patchKnowledge,
} from "./knowledge";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useKnowledgeApi = () => {
  const { axiosInstance } = useAxios();

  return {
    getAllBrainKnowledge: async (props: GetAllKnowledgeInputProps) =>
      getAllBrainKnowledge(props, axiosInstance),
    deleteKnowledge: async (props: DeleteKnowledgeInputProps) =>
      deleteKnowledge(props, axiosInstance),
    generateSignedUrlKnowledge: async (props: { knowledgeId: UUID }) =>
      generateSignedUrlKnowledge(props, axiosInstance),
    getFiles: async (parentId: UUID | null) =>
      getFiles(parentId, axiosInstance),
    addFolder: async (addFolderData: AddFolderData) =>
      addFolder(addFolderData, axiosInstance),
    patchKnowledge: async (knowledgeId: UUID, data: KMSElement) =>
      patchKnowledge(knowledgeId, data, axiosInstance),
  };
};
