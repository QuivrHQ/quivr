/* eslint-disable max-lines */
"use client";

import { CopyButton } from "@/lib/components/ui/CopyButton";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./ApiKeyConfig.module.scss";
import { useApiKeyConfig } from "./hooks/useApiKeyConfig";

export const ApiKeyConfig = (): JSX.Element => {
  const { apiKey, handleCopyClick, handleCreateClick } = useApiKeyConfig();

  const createNewApiKey = async () => {
    await handleCreateClick();
  };

  return (
    <div>
      {apiKey === "" ? (
        <QuivrButton
          iconName="key"
          color="primary"
          label="Create new key"
          onClick={() => createNewApiKey()}
          small={true}
        />
      ) : (
        <div className={styles.response_wrapper}>
          <span>{apiKey}</span>
          <CopyButton handleCopy={handleCopyClick} size="small" />
        </div>
      )}
    </div>
  );
};
