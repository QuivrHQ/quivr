import { createContext, PropsWithChildren } from "react";

import { BrainConfigContextType } from "../types";

export const BrainConfigContextMock = createContext<
  BrainConfigContextType | undefined
>(undefined);

export const BrainConfigProviderMock = ({
  children,
}: PropsWithChildren): JSX.Element => {
  return (
    <BrainConfigContextMock.Provider
      value={{
        config: {
          model: "gpt-3.5-turbo-0613",
          temperature: 0,
          maxTokens: 256,
          keepLocal: true,
        },
        updateConfig: () => void 0,
        resetConfig: () => void 0,
      }}
    >
      {children}
    </BrainConfigContextMock.Provider>
  );
};
