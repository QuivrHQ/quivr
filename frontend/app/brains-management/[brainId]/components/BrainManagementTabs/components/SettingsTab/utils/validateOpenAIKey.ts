import axios from "axios";

import { ToastData } from "@/lib/components/ui/Toast/domain/types";
import { getAxiosErrorParams } from "@/lib/helpers/getAxiosErrorParams";

export const getOpenAIKeyValidationStatusCode = async (
  key: string
): Promise<number> => {
  const url = "https://api.openai.com/v1/chat/completions";
  const headers = {
    Authorization: `Bearer ${key}`,
    "Content-Type": "application/json",
  };

  const data = JSON.stringify({
    model: "gpt-3.5-turbo",
    messages: [
      {
        role: "user",
        content: "Hello!",
      },
    ],
  });

  try {
    await axios.post(url, data, { headers });

    return 200;
  } catch (error) {
    return getAxiosErrorParams(error)?.status ?? 400;
  }
};

type ErrorMessages = {
  badApiKeyError: string;
  invalidApiKeyError: string;
};

export const validateOpenAIKey = async (
  openai_api_key: string | undefined,
  errorMessages: ErrorMessages,
  publish: (toast: ToastData) => void
): Promise<boolean> => {
  if (openai_api_key !== undefined) {
    const keyValidationStatusCode = await getOpenAIKeyValidationStatusCode(
      openai_api_key
    );

    if (keyValidationStatusCode !== 200) {
      if (keyValidationStatusCode === 401) {
        publish({
          variant: "danger",
          text: errorMessages.badApiKeyError,
        });
      }

      if (keyValidationStatusCode === 429) {
        publish({
          variant: "danger",
          text: errorMessages.invalidApiKeyError,
        });
      }

      return false;
    }

    return true;
  }

  return false;
};
