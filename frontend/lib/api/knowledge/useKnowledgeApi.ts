import { UUID } from "crypto";

import { useAxios } from "@/lib/hooks";

import {
  deleteKnowledge,
  DeleteKnowledgeInputProps,
  generateSignedUrlKnowledge,
  getAllBrainKnowledge,
  GetAllKnowledgeInputProps,
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
  };
};
