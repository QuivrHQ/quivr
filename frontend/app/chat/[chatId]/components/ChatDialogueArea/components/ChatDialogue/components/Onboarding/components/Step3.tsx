import { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { OnboardingState } from "@/lib/context/OnboardingContext/types";
import { useOnboardingContext } from "@/lib/hooks/useOnboardingContext";

import { MessageRow } from "../../QADisplay";
import { checkIfShouldDisplayStep } from "../helpers/checkIfShouldDisplayStep";
import { useStreamText } from "../hooks/useStreamText";
import { stepsContainerStyle } from "../styles";

const stepId: OnboardingState = "UPLOADED";

export const Step3 = (): JSX.Element => {
  const { currentStep } = useOnboardingContext();
  const shouldStepBeDisplayed = checkIfShouldDisplayStep({
    currentStep,
    step: stepId,
  });

  const { t } = useTranslation(["chat"]);
  const firstMessage = t("onboarding.last_step");
  const secondMessageStream = t("onboarding.ask_question_to_file");
  const shouldStreamMessage = currentStep === stepId;

  const { streamingText: streamingAssistantMessage, isDone: isAssistantDone } =
    useStreamText({
      text: firstMessage,
      enabled: shouldStepBeDisplayed,
      shouldStream: shouldStreamMessage,
    });

  const { streamingText: firstMessageStream } = useStreamText({
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
        <p>{firstMessageStream}</p>
      </div>
    </MessageRow>
  );
};
