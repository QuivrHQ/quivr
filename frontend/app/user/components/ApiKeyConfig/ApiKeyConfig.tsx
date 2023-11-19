/* eslint-disable max-lines */
"use client";

import { useTranslation } from "react-i18next";
import { FaCopy } from "react-icons/fa";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";

import { useApiKeyConfig } from "./hooks/useApiKeyConfig";

export const ApiKeyConfig = (): JSX.Element => {
  const {
    apiKey,
    handleCopyClick,
    handleCreateClick,
    
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
     
    </>
  );
};
