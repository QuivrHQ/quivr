import { act, renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useLogin } from "../useLogin";

const mockSignInWithPassword = vi.fn(() => ({ error: null }));

const mockUseSupabase = () => ({
  supabase: {
    auth: {
      signInWithPassword: mockSignInWithPassword,
    },
  },
});

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

describe("useLogin", () => {
  it("should call signInWithPassword with user email and password", async () => {
    const { result } = renderHook(() => useLogin());

    const email = "user@quivr.com";
    const password = "password";

    act(() => result.current.setEmail(email));
    act(() => result.current.setPassword(password));

    await act(() => result.current.handleLogin());

    expect(mockSignInWithPassword).toHaveBeenCalledTimes(1);
    expect(mockSignInWithPassword).toHaveBeenCalledWith({
      email,
      password,
    });
  });
});
