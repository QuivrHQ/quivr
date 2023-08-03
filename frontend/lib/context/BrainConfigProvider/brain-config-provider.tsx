/* eslint-disable */
"use client";

import { createContext, useEffect, useState } from "react";

import { removeUndefined } from "@/lib/helpers/removeUndefined";
import {
  getBrainConfigFromLocalStorage,
  saveBrainConfigInLocalStorage,
} from "./helpers/brainConfigLocalStorage";
import { BrainConfig, BrainConfigContextType } from "./types";

export const BrainConfigContext = createContext<
  BrainConfigContextType | undefined
>(undefined);

const defaultBrainConfig: BrainConfig = {
  model: "gpt-3.5-turbo-0613",
  temperature: 0,
  maxTokens: 256,
  keepLocal: true,
  anthropicKey: undefined,
  backendUrl: undefined,
  openAiKey: undefined,
  supabaseKey: undefined,
  supabaseUrl: undefined,
  prompt_id: undefined,
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
        ...removeUndefined(newConfig),
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
