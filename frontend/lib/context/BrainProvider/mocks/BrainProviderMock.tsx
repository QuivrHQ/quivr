import { createContext, PropsWithChildren } from "react";

import { BrainContextType } from "../types";

export const BrainContextMock = createContext<BrainContextType | undefined>(
  undefined
);

export const BrainProviderMock = ({
  children,
}: PropsWithChildren): JSX.Element => {
  return (
    <BrainContextMock.Provider
      value={{
        allBrains: [],
        publicPrompts:[],
        currentBrain: undefined,
        //@ts-ignore we are not using the functions in tests
        createBrain: () => void 0,
        //@ts-ignore we are not using the functions in tests
        deleteBrain: () => void 0,
        //@ts-ignore we are not using the functions in tests
        currentBrainId: undefined,
        //@ts-ignore we are not using the functions in tests
        fetchAllBrains: () => void 0,
        //@ts-ignore we are not using the functions in tests
        getBrainWithId: () => void 0,
        //@ts-ignore we are not using the functions in tests
        setActiveBrain: () => void 0,
        //@ts-ignore we are not using the functions in tests
        setDefaultBrain: () => void 0,
      }}
    >
      {children}
    </BrainContextMock.Provider>
  );
};
