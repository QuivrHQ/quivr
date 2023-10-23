import axios from "axios";

import { DEFAULT_CMS_URL } from "@/lib/config/CONSTANTS";

import { getDemoVideoUrl } from "./demoVideo";
import { getSecurityQuestions } from "./securityQuestion";
import { getTestimonials } from "./testimonials";
import { getUseCases } from "./useCases";

const axiosInstance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_CMS_URL ?? DEFAULT_CMS_URL}`,
});

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useCmsApi = () => {
  return {
    getTestimonials: () => getTestimonials(axiosInstance),
    getUseCases: () => getUseCases(axiosInstance),
    getDemoVideoUrl: () => getDemoVideoUrl(axiosInstance),
    getSecurityQuestions: () => getSecurityQuestions(axiosInstance),
  };
};
