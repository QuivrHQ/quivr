import { Onboarding } from "@/lib/types/Onboarding";

export type QuestionId = keyof Omit<Onboarding, "onboarding_a">;
