"use client";

import { setEmptyStringsUndefined } from "@/lib/helpers/setEmptyStringsUndefined";
import { createContext, useEffect, useState } from "react";
import {
  getBrainConfigFromLocalStorage,
  saveBrainConfigInLocalStorage,
} from "./helpers/brainConfigLocalStorage";
import { BrainConfig, ConfigContext } from "./types";

export const BrainConfigContext = createContext<ConfigContext | undefined>(
  undefined
);

const defaultBrainConfig: BrainConfig = {
  model: "gpt-3.5-turbo",
  temperature: 0,
  maxTokens: 500,
  keepLocal: true,
  anthropicKey: undefined,
  backendUrl: undefined,
  openAiKey: undefined,
  supabaseKey: undefined,
  supabaseUrl: undefined,
};

export const BrainConfigProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [brainConfig, setBrainConfig] =
    useState<BrainConfig>(defaultBrainConfig);

  const updateConfig = (newConfig: Partial<BrainConfig>) => {
    setBrainConfig((config) => {
      const updatedConfig: BrainConfig = {
        ...config,
        ...setEmptyStringsUndefined(newConfig),
      };
      saveBrainConfigInLocalStorage(updatedConfig);

      return updatedConfig;
    });
  };

  const resetConfig = () => {
    updateConfig(defaultBrainConfig);
  };

  useEffect(() => {
    setBrainConfig(getBrainConfigFromLocalStorage() ?? defaultBrainConfig);
  }, []);

  return (
    <BrainConfigContext.Provider
      value={{ config: brainConfig, updateConfig, resetConfig }}
    >
      {children}
    </BrainConfigContext.Provider>
  );
};
