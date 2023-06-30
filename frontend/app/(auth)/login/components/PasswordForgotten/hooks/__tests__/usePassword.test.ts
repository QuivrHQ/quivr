import { act, renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { usePasswordForgotten } from "../usePasswordForgotten";

const mockResetPasswordForEmail = vi.fn(() => ({ error: null }));

const mockUseSupabase = () => ({
  supabase: {
    auth: {
      resetPasswordForEmail: mockResetPasswordForEmail,
    },
  },
});

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

const setEmail = vi.fn();

describe("usePassword", () => {
  it("should not call resetPasswordForEmail if email is empty", async () => {
    const { result } = renderHook(() =>
      usePasswordForgotten({
        email: "",
        setEmail,
      })
    );

    await act(() => result.current.handleRecoverPassword());
    expect(mockResetPasswordForEmail).toHaveBeenCalledTimes(0);
  });

  it("should call resetPasswordForEmail with proper arguments", async () => {
    const email = "user@quivr.app";
    const { result } = renderHook(() =>
      usePasswordForgotten({
        email,
        setEmail,
      })
    );

    await act(() => result.current.handleRecoverPassword());
    expect(mockResetPasswordForEmail).toHaveBeenCalledTimes(1);
    expect(mockResetPasswordForEmail).toHaveBeenCalledWith(email, {
      redirectTo: `${window.location.origin}/recover-password`,
    });
  });
});
