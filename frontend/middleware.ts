import { createMiddlewareSupabaseClient } from "@supabase/auth-helpers-nextjs";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
// import type { Database } from '@/lib/database.types'

export const middleware = async (req: NextRequest): Promise<NextResponse> => {
  const res = NextResponse.next();
  const supabase = createMiddlewareSupabaseClient({ req, res });
  await supabase.auth.getSession();

  return res;
};
