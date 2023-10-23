import { AxiosInstance } from "axios";

type CmsVideo = {
  data: {
    attributes: {
      Video: {
        data: {
          attributes: {
            url: string;
          };
        };
      };
    };
  };
};

export const getDemoVideoUrl = async (
  axiosInstance: AxiosInstance
): Promise<string> => {
  const response = await axiosInstance.get<CmsVideo>(
    "/api/demo-video?populate=Video"
  );

  return response.data.data.attributes.Video.data.attributes.url;
};
