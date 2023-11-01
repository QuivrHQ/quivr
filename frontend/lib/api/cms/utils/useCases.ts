import { AxiosInstance } from "axios";

import { UseCase } from "@/lib/types/UseCase";

type CmsUseCases = {
  data: {
    id: number;
    attributes: {
      description: string;
      createdAt: string;
      updatedAt: string;
      publishedAt: string;
      name: string;
      locale: string;
      discussions: {
        data: {
          id: number;
          attributes: {
            Question: string;
            Answer: string;
            createdAt: string;
            updatedAt: string;
            publishedAt: string;
            locale: string;
          };
        }[];
      };
    };
  }[];
  meta: {
    pagination: {
      page: number;
      pageSize: number;
      pageCount: number;
      total: number;
    };
  };
};

const mapCmsUseCasesToUsecase = (jsonData: CmsUseCases): UseCase[] => {
  return jsonData.data.map((item) => ({
    id: item.id.toString(),
    description: item.attributes.description,
    name: item.attributes.name,
    createdAt: item.attributes.createdAt,
    updatedAt: item.attributes.updatedAt,
    publishedAt: item.attributes.publishedAt,
    locale: item.attributes.locale,
    discussions: item.attributes.discussions.data.map((discussion) => ({
      question: discussion.attributes.Question,
      answer: discussion.attributes.Answer,
      discussionCreatedAt: discussion.attributes.createdAt,
    })),
  }));
};

export const getUseCases = async (
  axiosInstance: AxiosInstance
): Promise<UseCase[]> => {
  const response = await axiosInstance.get<CmsUseCases>(
    "/api/use-cases?populate=discussions"
  );

  return mapCmsUseCasesToUsecase(response.data);
};
