import { SubmitHandler, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";
import Spinner from "@/lib/components/ui/Spinner";
import { emailPattern } from "@/lib/config/patterns";

import { usePostContactSales } from "../hooks/usePostContactSales";

export const ContactForm = (): JSX.Element => {
  const { t } = useTranslation("contact", { keyPrefix: "form" });

  const { register, handleSubmit, formState } = useForm({
    defaultValues: { email: "", message: "" },
  });

  const postEmail = usePostContactSales();

  const onSubmit: SubmitHandler<{ email: string; message: string }> = (
    data,
    event
  ) => {
    event?.preventDefault();
    postEmail.mutate({
      customer_email: data.email,
      content: data.message,
    });
  };

  if (postEmail.isSuccess) {
    return (
      <div className="flex flex-col items-center justify-center gap-5">
        <h2 className="text-2xl font-bold">{t("thank_you")}</h2>
        <p className="text-center text-zinc-400">{t("thank_you_text")}</p>
      </div>
    );
  }

  if (postEmail.isPending) {
    return <Spinner />;
  }

  return (
    <form
      className="flex flex-col gap-5 justify-stretch w-full"
      onSubmit={(event) => void handleSubmit(onSubmit)(event)}
    >
      <fieldset className="grid grid-cols-1 sm:grid-cols-3 gap-2 w-full gap-y-5">
        <label className="font-bold" htmlFor="email">
          {t("email")}
          <sup>*</sup>:
        </label>
        <input
          type="email"
          {...register("email", {
            pattern: emailPattern,
            required: true,
          })}
          placeholder="jane@example.com"
          className="col-span-2 bg-[#FCFAF6] rounded-md p-2"
        />
        <label className="font-bold" htmlFor="message">
          {t("question")}
          <sup>*</sup>:
        </label>
        <textarea
          {...register("message", {
            required: true,
          })}
          rows={3}
          placeholder={t("placeholder_question")}
          className="col-span-2 bg-[#FCFAF6] rounded-md p-2"
        ></textarea>
      </fieldset>

      <Button
        className="self-end rounded-full bg-primary flex items-center justify-center gap-2 border-none hover:bg-primary/90"
        disabled={!formState.isValid}
      >
        {t("submit")}
        <LuChevronRight size={24} />
      </Button>
    </form>
  );
};
