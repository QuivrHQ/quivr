"use client";

import { createContext, useEffect, useState } from "react";
import {
  getBrainConfigFromLocalStorage,
  saveBrainConfigInLocalStorage,
} from "./helpers/brainConfigLocalStorage";
import { BrainConfig, ConfigContext } from "./types";

export const BrainConfigContext = createContext<ConfigContext | undefined>(
  undefined
);

export const BrainConfigProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [brainConfig, setBrainConfig] = useState<BrainConfig>({
    model: "gpt-3.5-turbo",
    temperature: 0,
    maxTokens: 500,
    anthropicKey: undefined,
    backendUrl: undefined,
    openAiKey: undefined,
    keepLocal: true,
  });

  const updateConfig = (newConfig: Partial<BrainConfig>) => {
    setBrainConfig((config) => {
      const updatedConfig: BrainConfig = {
        ...config,
        ...newConfig,
      };
      saveBrainConfigInLocalStorage(updatedConfig);

      return updatedConfig;
    });
  };

  useEffect(() => {
    setBrainConfig(getBrainConfigFromLocalStorage() ?? defaultBrainConfig);
  }, []);

  return (
    <BrainConfigContext.Provider value={{ config: brainConfig, updateConfig }}>
      {children}
    </BrainConfigContext.Provider>
  );
};
