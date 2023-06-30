import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useGoogleLogin } from "../useGoogleLogin";

const mockSignInWithOAuth = vi.fn(() => ({ error: null }));

const mockUseSupabase = () => ({
  supabase: {
    auth: {
      signInWithOAuth: mockSignInWithOAuth,
    },
  },
});

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

describe("useGoogleLogin", () => {
  it("should call signInWithOAuth", async () => {
    const { result } = renderHook(() => useGoogleLogin());

    await result.current.signInWithGoogle();

    expect(mockSignInWithOAuth).toHaveBeenCalledTimes(1);
  });
});
