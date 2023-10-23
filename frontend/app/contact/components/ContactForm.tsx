import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

export const ContactForm = (): JSX.Element => {
  const [email, setEmail] = useState<string>("");
  const [message, setMessage] = useState<string>("");
  const [submitted, setSubmitted] = useState<boolean>(false);
  const { t } = useTranslation("contact", { keyPrefix: "form" });

  const handleSubmit = (ev: React.FormEvent) => {
    ev.preventDefault();
    setSubmitted(true);
    console.log("submitting", email, message);
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
    <form className="flex flex-col gap-5 justify-stretch w-full">
      <fieldset className="grid grid-cols-1 sm:grid-cols-3 gap-2 w-full gap-y-5">
        <label className="font-bold" htmlFor="email">
          {t("email")}
          <sup>*</sup>:
        </label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(ev) => setEmail(ev.target.value)}
          placeholder="jane@example.com"
          className="col-span-2 bg-[#FCFAF6] rounded-md p-2"
          required
        />
        <label className="font-bold" htmlFor="message">
          {t("question")}
          <sup>*</sup>:
        </label>
        <textarea
          id="message"
          value={message}
          rows={3}
          onChange={(ev) => setMessage(ev.target.value)}
          placeholder={t("placeholder_question")}
          className="col-span-2 bg-[#FCFAF6] rounded-md p-2"
          required
        ></textarea>
      </fieldset>

      <Button
        onClick={handleSubmit}
        className="self-end rounded-full bg-primary flex items-center justify-center gap-2 border-none hover:bg-primary/90"
      >
        {t("submit")}
        <LuChevronRight size={24} />
      </Button>
    </form>
  );
};
