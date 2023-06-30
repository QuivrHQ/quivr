import { act, renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useMagicLinkLogin } from "../useMagicLinkLogin";

const mockSignInWithOtp = vi.fn(() => ({ error: null }));

const mockUseSupabase = () => ({
  supabase: {
    auth: {
      signInWithOtp: mockSignInWithOtp,
    },
  },
});

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));
const setEmail = vi.fn();

describe("useMagicLinkLogin", () => {
  it("should not call signInWithOtp if email is empty", async () => {
    const { result } = renderHook(() =>
      useMagicLinkLogin({
        email: "",
        setEmail,
      })
    );
    await act(() => result.current.handleMagicLinkLogin());
    expect(mockSignInWithOtp).toHaveBeenCalledTimes(0);
  });

  it("should call signInWithOtp with proper arguments", async () => {
    const email = "user@quivr.app";
    const { result } = renderHook(() =>
      useMagicLinkLogin({
        email,
        setEmail,
      })
    );
    await result.current.handleMagicLinkLogin();
    expect(mockSignInWithOtp).toHaveBeenCalledTimes(1);
    expect(mockSignInWithOtp).toHaveBeenCalledWith({
      email,
      options: { emailRedirectTo: window.location.hostname },
    });
  });
});
