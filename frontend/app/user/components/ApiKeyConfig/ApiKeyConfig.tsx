/* eslint-disable max-lines */
"use client";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";
import Field from "@/lib/components/ui/Field";

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

  return (
    <>
      <Divider text="API Key Config" className="mt-4" />
      <div className="flex justify-center items-center mt-4">
        <div className="flex items-center space-x-4">
          {apiKey === "" && (
            <Button
              data-testid="create-new-key"
              variant="secondary"
              onClick={() => void handleCreateClick()}
            >
              Create New Key
            </Button>
          )}
        </div>
        {apiKey !== "" && (
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">{apiKey}</span>
            <Button
              data-testid="copy-api-key-button"
              variant="secondary"
              onClick={handleCopyClick}
            >
              📋
            </Button>
          </div>
        )}
      </div>

      <Divider text="OpenAI Key" className="mt-4 mb-4" />
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void changeOpenAiApiKey();
        }}
      >
        <Field
          name="openAiApiKey"
          placeholder="Open AI Key"
          className="w-full"
          value={openAiApiKey ?? ""}
          data-testid="open-ai-api-key"
          onChange={(e) => setOpenAiApiKey(e.target.value)}
        />
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
    </>
  );
};
