import { useContext } from "react";

import { SupabaseContext } from "../supabase-provider";
import { SupabaseContextType } from "../types";

export const useSupabase = (): SupabaseContextType => {
  const context = useContext(SupabaseContext);

  if (context === undefined) {
    throw new Error("useSupabase must be used inside SupabaseProvider");
  }

  return context;
};
