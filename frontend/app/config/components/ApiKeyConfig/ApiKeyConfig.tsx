"use client";

import Button from "@/lib/components/ui/Button";

import { useApiKeyConfig } from "./hooks/useApiKeyConfig";

export const ApiKeyConfig = (): JSX.Element => {
  const { apiKey, handleCopyClick, handleCreateClick } = useApiKeyConfig();

  return (
    <>
      <div className="border-b border-gray-300 w-full max-w-xl mb-8">
        <p className="text-center text-gray-600 uppercase tracking-wide font-semibold">
          API Key Config
        </p>
      </div>
      <div className="flex justify-between items-center">
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
    </>
  );
};
