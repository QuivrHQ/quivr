import { TFunction } from "i18next";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";

import { validateOpenAIKey } from "./validateOpenAIKey";

export const checkOpenAiKey = async (
  openai_api_key: string | undefined,
  publish: (toast: ToastData) => void,
  t: TFunction<["translation", "brain", "config"]>
): Promise<void> => {
  if (
    openai_api_key !== undefined &&
    openai_api_key !== "" &&
    !(await validateOpenAIKey(
      openai_api_key,
      {
        badApiKeyError: t("incorrectApiKey", { ns: "config" }),
        invalidApiKeyError: t("invalidApiKeyError", { ns: "config" }),
      },
      publish
    ))
  ) {
    return;
  }
};
