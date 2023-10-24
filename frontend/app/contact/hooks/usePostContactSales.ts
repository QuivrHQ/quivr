import { useMutation, UseMutationResult } from "@tanstack/react-query";

import { useAxios } from "@/lib/hooks";
import { useToast } from "@/lib/hooks/useToast";

interface ContactSalesDto {
  customer_email: string;
  content: string;
}

export const usePostContactSales = (): UseMutationResult<
  void,
  unknown,
  ContactSalesDto
> => {
  const { axiosInstance } = useAxios();
  const toast = useToast();

  return useMutation({
    mutationKey: ["contactSales"],
    mutationFn: async (data) => {
      await axiosInstance.post("/contact", data);
    },
    onError: () => {
      toast.publish({
        text: "There was an error sending your message. Please try again later.",
        variant: "danger",
      });
    },
  });
};
