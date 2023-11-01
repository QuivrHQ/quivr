import { AxiosInstance } from "axios";

import { SecurityQuestion } from "@/lib/types/SecurityQuestion";

type CmsSecurityQuestions = {
  data: {
    id: number;
    attributes: {
      createdAt: string;
      updatedAt: string;
      publishedAt: string;
      locale: string;
      question: string;
      answer: string;
    };
  }[];
};

const mapCmsSecurityQuestionToSecurityQuestion = (
  cmsSecurityQuestions: CmsSecurityQuestions
): SecurityQuestion[] =>
  cmsSecurityQuestions.data.map((cmsSecurityQuestion) => ({
    question: cmsSecurityQuestion.attributes.question,
    answer: cmsSecurityQuestion.attributes.answer,
  }));

export const getSecurityQuestions = async (
  axiosInstance: AxiosInstance
): Promise<SecurityQuestion[]> => {
  const response = await axiosInstance.get<CmsSecurityQuestions>(
    "/api/security-questions"
  );

  return mapCmsSecurityQuestionToSecurityQuestion(response.data);
};
