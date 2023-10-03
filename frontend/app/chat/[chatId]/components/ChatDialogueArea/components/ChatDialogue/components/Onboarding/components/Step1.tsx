import Link from "next/link";
import { useTranslation } from "react-i18next";
import { RiDownloadLine } from "react-icons/ri";

import Button from "@/lib/components/ui/Button";

import { MessageRow } from "../../QADisplay";
import { checkIfShouldDisplayStep } from "../helpers/checkIfShouldDisplayStep";
import { useStreamText } from "../hooks/useStreamText";

type Step1Props = {
  currentStep: "DOWNLOAD" | "UPLOAD";
};

export const Step1 = ({ currentStep }: Step1Props): JSX.Element => {
  const shouldStepBeDisplayed = checkIfShouldDisplayStep({
    currentStep,
    step: "STEP_1",
  });

  const { t } = useTranslation(["chat"]);
  const assistantMessage = t("onboarding.step_1_message_1");
  const step1Text = t("onboarding.step_1_message_2");

  const { streamingText: streamingAssistantMessage, isDone: isAssistantDone } =
    useStreamText({
      text: assistantMessage,
      enabled: shouldStepBeDisplayed,
    });
  const { streamingText: streamingStep1Text, isDone: isStep1Done } =
    useStreamText({
      text: step1Text,
      enabled: isAssistantDone && shouldStepBeDisplayed,
    });

  return (
    <MessageRow speaker={"assistant"} brainName={"Quivr"}>
      <p>{streamingAssistantMessage}</p>
      <div>
        {streamingStep1Text}
        {isStep1Done && isAssistantDone && (
          <Link
            href="/documents/doc.pdf"
            download
            target="_blank"
            referrerPolicy="no-referrer"
          >
            <Button className="bg-black p-2 ml-2 rounded-full inline-flex">
              <RiDownloadLine />
            </Button>
          </Link>
        )}
      </div>
    </MessageRow>
  );
};
