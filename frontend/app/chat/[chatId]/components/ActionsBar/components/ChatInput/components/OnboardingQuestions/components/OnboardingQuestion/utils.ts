import { Translations } from "@/lib/config/LocaleConfig/resources";

import { QuestionId } from "../../types";

export const questionIdToTradPath: Record<
  QuestionId,
  keyof Pick<
    Translations["vaccineTruth"]["onboarding"],
    "virus_origin" | "vaccine_effect" | "vaccine_antidote"
  >
> = {
  onboarding_b1: "virus_origin",
  onboarding_b2: "vaccine_effect",
  onboarding_b3: "vaccine_antidote",
};
