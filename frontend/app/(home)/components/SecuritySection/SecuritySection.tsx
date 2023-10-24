import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useTranslation } from "react-i18next";
import { LuChevronRight, LuShieldCheck } from "react-icons/lu";

import { SECURITY_QUESTIONS_DATA_KEY } from "@/lib/api/cms/config";
import { useCmsApi } from "@/lib/api/cms/useCmsApi";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/lib/components/ui/Accordion";
import Button from "@/lib/components/ui/Button";
import Spinner from "@/lib/components/ui/Spinner";

import { useHomepageTracking } from "../../hooks/useHomepageTracking";

export const SecuritySection = (): JSX.Element => {
  const { t } = useTranslation("home", {
    keyPrefix: "security",
  });
  const { onLinkClick } = useHomepageTracking();

  const { getSecurityQuestions } = useCmsApi();

  const { data: securityQuestions = [] } = useQuery({
    queryKey: [SECURITY_QUESTIONS_DATA_KEY],
    queryFn: getSecurityQuestions,
  });

  if (securityQuestions.length === 0) {
    return <Spinner />;
  }

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
        <Link
          href="/signup"
          onClick={(event) => {
            onLinkClick({
              href: "/signup",
              label: "SIGN_UP",
              event,
            });
          }}
        >
          <Button className="rounded-full">
            {t("cta")}
            <LuChevronRight size={24} />
          </Button>
        </Link>
      </div>
    </>
  );
};
