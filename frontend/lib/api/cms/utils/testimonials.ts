import { AxiosInstance } from "axios";

import { Testimonial } from "@/lib/types/testimonial";

type CmsTestimonials = {
  data: {
    id: number;
    attributes: {
      url: string;
      jobTitle: string;
      content: string;
      name: string;
      profilePicture: string | null;
      socialMedia: string;
      createdAt: string;
      updatedAt: string;
      publishedAt: string;
      locale: string;
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

const mapCmsTestimonialsToTestimonial = (
  testimonials: CmsTestimonials
): Testimonial[] => {
  return testimonials.data.map((item) => ({
    socialMedia: item.attributes.socialMedia as "x" | "linkedin",
    url: item.attributes.url,
    jobTitle: item.attributes.jobTitle,
    content: item.attributes.content,
    name: item.attributes.name,
    profilePicture: item.attributes.profilePicture ?? undefined,
  }));
};

export const getTestimonials = async (
  axiosInstance: AxiosInstance
): Promise<Testimonial[]> => {
  const response = await axiosInstance.get<CmsTestimonials>(
    "/api/testimonials"
  );

  return mapCmsTestimonialsToTestimonial(response.data);
};
