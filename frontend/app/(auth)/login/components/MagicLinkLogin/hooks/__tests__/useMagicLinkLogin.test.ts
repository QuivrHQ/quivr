import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useMagicLinkLogin } from "../useMagicLinkLogin";

const mockSignInWithOtp = vi.fn(() => ({ error: null }));

const mockUseSupabase = () => ({
  supabase: {
    auth: {
      signInWithOtp: mockSignInWithOtp,
    },
  },
});
const email = "user@quivr.app";
const watchMock = vi.fn(() => email);
vi.mock("react-hook-form", async () => {
  const actual = await vi.importActual<typeof import("react-hook-form")>(
    "react-hook-form"
  );

  return {
    ...actual,
    useForm: () => ({
      ...actual.useForm(),
      watch: watchMock,
    }),
  };
});

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

describe("useMagicLinkLogin", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should not call signInWithOtp if email is empty", async () => {
    watchMock.mockReturnValueOnce("");
    const { result } = renderHook(() => useMagicLinkLogin());
    await act(() => result.current.handleMagicLinkLogin());
    expect(mockSignInWithOtp).toHaveBeenCalledTimes(0);
  });

  it("should call signInWithOtp with proper arguments", async () => {
    const { result } = renderHook(() => useMagicLinkLogin());
    await result.current.handleMagicLinkLogin();
    expect(mockSignInWithOtp).toHaveBeenCalledTimes(1);
    expect(mockSignInWithOtp).toHaveBeenCalledWith({
      email,
      options: { emailRedirectTo: window.location.hostname },
    });
  });
});
