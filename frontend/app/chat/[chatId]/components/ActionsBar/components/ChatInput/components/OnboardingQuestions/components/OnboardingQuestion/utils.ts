import { Translations } from "@/lib/config/LocaleConfig/resources";

import { QuestionId } from "../../types";

export const questionIdToTradPath: Record<
  QuestionId,
  keyof Translations["chat"]["onboarding"]
> = {
  onboarding_b1: "how_to_use_quivr",
  onboarding_b2: "what_is_quivr",
  onboarding_b3: "what_is_brain",
};
