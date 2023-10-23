import React, { useState } from "react";
import { FieldValues, SubmitHandler, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

export const ContactForm = (): JSX.Element => {
  const [submitted, setSubmitted] = useState<boolean>(false);
  const { t } = useTranslation("contact", { keyPrefix: "form" });

  const { register, handleSubmit, formState } = useForm({
    defaultValues: { email: "", message: "" },
  });

  const emailPattern = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;

  const onSubmit: SubmitHandler<FieldValues> = (data) => {
    setSubmitted(true);
    console.log("submitting", data.email, data.message);
  };

  if (submitted) {
    return (
      <div className="flex flex-col items-center justify-center gap-5">
        <h2 className="text-2xl font-bold">{t("thank_you")}</h2>
        <p className="text-center text-zinc-400">{t("thank_you_text")}</p>
      </div>
    );
  }

  return (
    <form
      className="flex flex-col gap-5 justify-stretch w-full"
      onSubmit={() => void handleSubmit(onSubmit)()}
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
