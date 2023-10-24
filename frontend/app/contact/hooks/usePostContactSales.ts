import { useMutation, UseMutationResult } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

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
  const { t } = useTranslation("contact", { keyPrefix: "form" });

  return useMutation({
    mutationKey: ["contactSales"],
    mutationFn: async (data) => {
      await axiosInstance.post("/contact", data);
    },
    onError: () => {
      toast.publish({
        text: t("sending_mail_error"),
        variant: "danger",
      });
    },
  });
};
