import React, { useState } from "react";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

export const ContactForm = (): JSX.Element => {
  const [email, setEmail] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const handleSubmit = () => {
    console.log("submitting", email, message);
  };

  return (
    <form className="flex flex-col gap-5 justify-stretch w-full">
      <fieldset className="grid grid-cols-1 sm:grid-cols-3 gap-2 w-full gap-y-5">
        <label className="font-bold" htmlFor="email">
          Work Email<sup>*</sup>:
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
          Question<sup>*</sup>:
        </label>
        <textarea
          id="message"
          value={message}
          rows={3}
          onChange={(ev) => setMessage(ev.target.value)}
          placeholder="How can we help you?"
          className="col-span-2 bg-[#FCFAF6] rounded-md p-2"
          required
        ></textarea>
      </fieldset>

      <Button
        onClick={handleSubmit}
        className="self-end rounded-full bg-primary flex items-center justify-center gap-2 border-none hover:bg-primary/90"
      >
        Contact
        <LuChevronRight size={24} />
      </Button>
    </form>
  );
};
