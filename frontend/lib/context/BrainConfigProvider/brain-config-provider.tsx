"use client";

import { createContext, useState } from "react";
import { BrainConfig, ConfigContext } from "./types";

export const BrainConfigContext = createContext<ConfigContext | undefined>(
  undefined
);

export const BrainConfigProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const [config, setConfig] = useState<BrainConfig>({
    model: "gpt-3.5-turbo",
    temperature: 0,
    maxTokens: 500,
    anthropicKey: undefined,
    backendUrl: undefined,
    openAiKey: undefined,
    keepLocal: true,
  });

  const updateConfig = (newConfig: Partial<BrainConfig>) => {
    setConfig({ ...config, ...newConfig });
  };

  return (
    <BrainConfigContext.Provider value={{ config, updateConfig }}>
      {children}
    </BrainConfigContext.Provider>
  );
};
