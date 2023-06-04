import { createMiddlewareSupabaseClient } from '@supabase/auth-helpers-nextjs'
import type { NextRequest } from 'next/server'
import { NextResponse } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareSupabaseClient({ req, res })

  try {
    await supabase.auth.getSession()
  } catch (error) {
    if (error instanceof Error && error.message === 'Invalid Refresh Token: Already Used') {
      // Attempt to sign the user out
      const { error: signOutError } = await supabase.auth.signOut()

      if (signOutError) {
        console.error("Error logging out:", signOutError.message)
      } else {
        console.log("Logged out successfully")
        return NextResponse.redirect('/')
      }
    }
  }

  return res
}
