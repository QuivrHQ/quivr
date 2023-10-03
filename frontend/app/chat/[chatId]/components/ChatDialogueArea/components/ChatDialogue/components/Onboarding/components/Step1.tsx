import Link from "next/link";
import { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { RiDownloadLine } from "react-icons/ri";

import Button from "@/lib/components/ui/Button";

import { MessageRow } from "../../QADisplay";
import { OnboardingState } from "../../types";
import { checkIfShouldDisplayStep } from "../helpers/checkIfShouldDisplayStep";
import { useStreamText } from "../hooks/useStreamText";
import { stepsContainerStyle } from "../styles";

type Step1Props = {
  currentStep: OnboardingState;
  changeStateTo: (state: OnboardingState) => void;
};

export const Step1 = ({
  currentStep,
  changeStateTo,
}: Step1Props): JSX.Element => {
  const shouldStepBeDisplayed = checkIfShouldDisplayStep({
    currentStep,
    step: "DOWNLOAD",
  });

  const { t } = useTranslation(["chat"]);
  const firstMessage = t("onboarding.download_message_1");
  const secondMessageStream = t("onboarding.download_message_2");

  const { streamingText: streamingAssistantMessage, isDone: isAssistantDone } =
    useStreamText({
      text: firstMessage,
      enabled: shouldStepBeDisplayed,
    });
  const { streamingText: firstMessageStrem, isDone: isStep1Done } =
    useStreamText({
      text: secondMessageStream,
      enabled: isAssistantDone && shouldStepBeDisplayed,
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
              onClick={() => changeStateTo("UPLOAD")}
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
