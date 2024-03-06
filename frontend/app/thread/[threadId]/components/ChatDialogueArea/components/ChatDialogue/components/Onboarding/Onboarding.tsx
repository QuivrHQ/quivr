import Link from "next/link";
import { useTranslation } from "react-i18next";
import { RiDownloadLine } from "react-icons/ri";

import Button from "@/lib/components/ui/Button";
import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";
import { useStreamText } from "@/lib/hooks/useStreamText";

import { stepsContainerStyle } from "./styles";

import { MessageRow } from "../QADisplay";

export const Onboarding = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const title = t("onboarding.title");
  const step1 = t("onboarding.step_1_1");
  const step1Details = t("onboarding.step_1_2");
  const step2 = t("onboarding.step_2");
  const step3 = t("onboarding.step_3");

  const { trackOnboardingEvent } = useOnboardingTracker();

  const { streamingText: titleStream, isDone: isTitleDisplayed } =
    useStreamText({
      text: title,
    });
  const { streamingText: firstStepStream, isDone: isStep1Done } = useStreamText(
    {
      text: step1,
      enabled: isTitleDisplayed,
    }
  );
  const { streamingText: firstStepDetailsStream, isDone: isStep1DetailsDone } =
    useStreamText({
      text: step1Details,
      enabled: isStep1Done,
    });

  const { streamingText: secondStepStream, isDone: isStep2Done } =
    useStreamText({
      text: step2,
      enabled: isStep1DetailsDone,
    });
  const { streamingText: thirdStepStream } = useStreamText({
    text: step3,
    enabled: isStep2Done,
  });

  return (
    <div className="flex flex-col gap-2 mb-3">
      <MessageRow speaker={"assistant"} brainName={"Quivr"}>
        <div className={stepsContainerStyle}>
          <p>{titleStream}</p>
          <div>
            <p>{firstStepStream}</p>
            <div>
              {firstStepDetailsStream}
              {isStep1DetailsDone && (
                <Link
                  href="/documents/quivr_documentation.pdf"
                  download
                  target="_blank"
                  referrerPolicy="no-referrer"
                  onClick={() => {
                    trackOnboardingEvent("QUIVR_DOCUMENTATION_DOWNLOADED");
                  }}
                >
                  <Button className="bg-black p-2 ml-2 rounded-full inline-flex">
                    <RiDownloadLine />
                  </Button>
                </Link>
              )}
            </div>
          </div>
          <p>{secondStepStream}</p>
          <p>{thirdStepStream}</p>
        </div>
      </MessageRow>
    </div>
  );
};
