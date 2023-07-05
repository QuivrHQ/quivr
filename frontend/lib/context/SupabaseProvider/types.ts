import { Session, SupabaseClient } from "@supabase/auth-helpers-nextjs";

export type SupabaseContextType = {
  supabase: SupabaseClient;
  session: Session | null;
};
