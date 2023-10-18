import Link from "next/link";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { LuChevronRight, LuShieldCheck } from "react-icons/lu";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/lib/components/ui/Accordion";
import Button from "@/lib/components/ui/Button";

import { securityQuestionsExamples } from "./data/securityQuestions";
import { SecurityQuestion } from "./types";

export const SecuritySection = (): JSX.Element => {
  const { t } = useTranslation("home", {
    keyPrefix: "security",
  });
  const [securityQuestions, setSecurityQuestions] = useState<
    SecurityQuestion[]
  >([]);

  useEffect(() => {
    setSecurityQuestions(securityQuestionsExamples);
  }, []);

  return (
    <>
      <div className="flex flex-1 w-full mb-10 p-6">
        <div className="hidden md:flex flex-1  items-center justify-center">
          <LuShieldCheck className="text-[150px]" />
        </div>
        <div className="flex-1">
          <Accordion type="multiple">
            {securityQuestions.map((question) => {
              return (
                <AccordionItem
                  value={question.question}
                  key={question.question}
                >
                  <AccordionTrigger>{question.question}</AccordionTrigger>
                  <AccordionContent>{question.answer}</AccordionContent>
                </AccordionItem>
              );
            })}
          </Accordion>
        </div>
      </div>
      <div className="flex md:justify-end w-full">
        <Link href="/signup">
          <Button className="rounded-full">
            {t("cta")}
            <LuChevronRight size={24} />
          </Button>
        </Link>
      </div>
    </>
  );
};
