import { createContext, PropsWithChildren } from "react";

import { SupabaseContextType } from "../types";

export const SupabaseContextMock = createContext<
  SupabaseContextType | undefined
>(undefined);

export const SupabaseProviderMock = ({
  children,
}: PropsWithChildren): JSX.Element => {
  return (
    <SupabaseContextMock.Provider
      value={{
        // @ts-ignore - we are not actually using these values in the tests
        supabase: {},
        // @ts-ignore - we are not actually using these values in the tests
        session: {},
      }}
    >
      {children}
    </SupabaseContextMock.Provider>
  );
};
