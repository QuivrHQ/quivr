/* eslint-disable max-lines */
"use client";

import { useTranslation } from "react-i18next";
import { FaCopy, FaInfoCircle } from "react-icons/fa";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import copyToClipboard from "@/lib/helpers/copyToClipboard";

import { useApiKeyConfig } from "./hooks/useApiKeyConfig";

export const ApiKeyConfig = (): JSX.Element => {
  const {
    apiKey,
    handleCopyClick,
    handleCreateClick,
    openAiApiKey,
    setOpenAiApiKey,
    changeOpenAiApiKey,
    changeOpenAiApiKeyRequestPending,
    userIdentity,
    removeOpenAiApiKey,
    hasOpenAiApiKey,
  } = useApiKeyConfig();
  const { t } = useTranslation(["config"]);

  return (
    <>
      <h3 className="font-semibold mb-2">Quivr {t("apiKey")}</h3>

      <div>
        {apiKey === "" ? (
          <Button
            data-testid="create-new-key"
            variant="secondary"
            onClick={() => void handleCreateClick()}
          >
            Create New Key
          </Button>
        ) : (
          <div className="flex items-center space-x-2">
            <Field name="quivrApiKey" disabled={true} value={apiKey} />
            <button data-testid="copy-api-key-button" onClick={handleCopyClick}>
              <FaCopy />
            </button>
          </div>
        )}
      </div>

      <hr className="my-8" />

      <div>
        <h3 className="font-semibold mb-2">OpenAI {t("apiKey")}</h3>
        <form
          className="mb-4"
          onSubmit={(event) => {
            event.preventDefault();
            void changeOpenAiApiKey();
          }}
        >
          <div className="flex items-center space-x-2">
            <Field
              name="openAiApiKey"
              placeholder="Open AI Key"
              className="w-full"
              value={openAiApiKey ?? ""}
              data-testid="open-ai-api-key-input"
              onChange={(e) => setOpenAiApiKey(e.target.value)}
            />
            <button
              hidden={!hasOpenAiApiKey}
              data-testid="copy-openai-api-key-button"
              onClick={() => void copyToClipboard(openAiApiKey)}
              type="button"
            >
              <FaCopy />
            </button>
          </div>

          <div className="mt-4 flex flex-row justify-between">
            {hasOpenAiApiKey && (
              <Button
                isLoading={changeOpenAiApiKeyRequestPending}
                variant="secondary"
                onClick={() => void removeOpenAiApiKey()}
              >
                Remove Key
              </Button>
            )}

            <Button
              data-testid="save-open-ai-api-key"
              isLoading={changeOpenAiApiKeyRequestPending}
              disabled={openAiApiKey === userIdentity?.openai_api_key}
            >
              Save Key
            </Button>
          </div>
        </form>

        <div className="flex space-x-2 bg-sky-100 dark:bg-gray-900 border border-sky-200 dark:border-gray-700  px-4 py-3 rounded relative max-w-md">
          <div className="text-xl font-semibold text-sky-600">
            <FaInfoCircle />
          </div>
          <div>
            <p>
              We will store your OpenAI API key, but we will not use it for any
              other purpose. However,{" "}
              <strong>we have not implemented any encryption logic yet</strong>
            </p>
          </div>
        </div>
      </div>
    </>
  );
};
