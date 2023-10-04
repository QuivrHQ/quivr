import { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { useOnboardingContext } from "@/lib/hooks/useOnboardingContext";

import { MessageRow } from "../../QADisplay";
import { checkIfShouldDisplayStep } from "../helpers/checkIfShouldDisplayStep";
import { useStreamText } from "../hooks/useStreamText";
import { stepsContainerStyle } from "../styles";

export const Step3 = (): JSX.Element => {
  const { currentStep } = useOnboardingContext();
  const shouldStepBeDisplayed = checkIfShouldDisplayStep({
    currentStep,
    step: "UPLOADED",
  });

  const { t } = useTranslation(["chat"]);
  const firstMessage = t("onboarding.last_step");
  const secondMessageStream = t("onboarding.ask_question_to_file");

  const { streamingText: streamingAssistantMessage, isDone: isAssistantDone } =
    useStreamText({
      text: firstMessage,
      enabled: shouldStepBeDisplayed,
    });

  const { streamingText: firstMessageStream } = useStreamText({
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
        <p>{firstMessageStream}</p>
      </div>
    </MessageRow>
  );
};
