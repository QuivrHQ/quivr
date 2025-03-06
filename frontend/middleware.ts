import { createMiddlewareSupabaseClient } from '@supabase/auth-helpers-nextjs';
import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';
// import type { Database } from '@/lib/database.types'

export const middleware = async (req: NextRequest): Promise<NextResponse> => {
  const res = NextResponse.next();
  const supabase = createMiddlewareSupabaseClient({ req, res });
  await supabase.auth.getSession();
  // Get current path
  // const currentPath = req.nextUrl.pathname;
  // Get the user from the session
  // const { data: { user } } = await supabase.auth.getUser();
  // const isSuperAdmin = user?.role === "super_admin";

  // // Redirect to search page if the user is not a super admin and tries to access the administrator page
  // if (currentPath === "/administrator" && !isSuperAdmin) {
  // 	return NextResponse.redirect(new URL("/search", req.url));
  // }

  return res;
};
