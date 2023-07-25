"use client";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";

import { useApiKeyConfig } from "./hooks/useApiKeyConfig";

export const ApiKeyConfig = (): JSX.Element => {
  const { apiKey, handleCopyClick, handleCreateClick } = useApiKeyConfig();

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
    </>
  );
};
