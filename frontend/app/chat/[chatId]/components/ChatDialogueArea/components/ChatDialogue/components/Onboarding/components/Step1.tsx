import Link from "next/link";
import { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { RiDownloadLine } from "react-icons/ri";

import Button from "@/lib/components/ui/Button";
import { OnboardingState } from "@/lib/context/OnboardingContext/types";
import { useOnboardingContext } from "@/lib/hooks/useOnboardingContext";

import { MessageRow } from "../../QADisplay";
import { checkIfShouldDisplayStep } from "../helpers/checkIfShouldDisplayStep";
import { useStreamText } from "../hooks/useStreamText";
import { stepsContainerStyle } from "../styles";

const stepId: OnboardingState = "DOWNLOAD";

export const Step1 = (): JSX.Element => {
  const { currentStep, setCurrentStep } = useOnboardingContext();
  const shouldStepBeDisplayed = checkIfShouldDisplayStep({
    currentStep,
    step: stepId,
  });

  const shouldStreamMessage = currentStep === stepId;

  const { t } = useTranslation(["chat"]);
  const firstMessage = t("onboarding.download_message_1");
  const secondMessageStream = t("onboarding.download_message_2");

  const { streamingText: streamingAssistantMessage, isDone: isAssistantDone } =
    useStreamText({
      text: firstMessage,
      enabled: shouldStepBeDisplayed,
      shouldStream: shouldStreamMessage,
    });
  const { streamingText: firstMessageStrem, isDone: isStep1Done } =
    useStreamText({
      text: secondMessageStream,
      enabled: isAssistantDone && shouldStepBeDisplayed,
      shouldStream: shouldStreamMessage,
    });

  if (!shouldStepBeDisplayed) {
    return <Fragment />;
  }

  return (
    <MessageRow speaker={"assistant"} brainName={"Quivr"}>
      <div className={stepsContainerStyle}>
        <p>{streamingAssistantMessage}</p>
        <div>
          {firstMessageStrem}
          {isStep1Done && isAssistantDone && (
            <Link
              href="/documents/doc.pdf"
              download
              target="_blank"
              referrerPolicy="no-referrer"
              onClick={() => setCurrentStep("UPLOAD")}
            >
              <Button className="bg-black p-2 ml-2 rounded-full inline-flex">
                <RiDownloadLine />
              </Button>
            </Link>
          )}
        </div>
      </div>
    </MessageRow>
  );
};
