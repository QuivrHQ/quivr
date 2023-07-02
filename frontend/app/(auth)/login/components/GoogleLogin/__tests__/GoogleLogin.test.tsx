import { fireEvent, render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { GoogleLoginButton } from "..";

//Mocking related hooks
const mockUseGoogleLogin = vi.fn(() => ({
  isPending: false,
  signInWithGoogle: vi.fn(),
}));

vi.mock("../hooks/useGoogleLogin", () => ({
  useGoogleLogin: () => mockUseGoogleLogin(),
}));

describe.concurrent("GoogleLoginButton", () => {
  it("renders correctly", () => {
    const { getByTestId } = render(<GoogleLoginButton />);

    const loginButton = getByTestId("google-login-button");

    expect(loginButton).toBeDefined();
  });

  it("calls signInWithGoogle on button click", () => {
    const mockSignInWithGoogle = vi.fn();
    mockUseGoogleLogin.mockReturnValue({
      isPending: false,
      signInWithGoogle: mockSignInWithGoogle,
    });

    const { getByTestId } = render(<GoogleLoginButton />);
    const loginButton = getByTestId("google-login-button");
    fireEvent.click(loginButton);

    expect(mockSignInWithGoogle).toHaveBeenCalledTimes(1);
  });

  it("doesn't call signInWithGoogle on button click when pending", () => {
    const mockSignInWithGoogle = vi.fn();
    mockUseGoogleLogin.mockReturnValue({
      isPending: true,
      signInWithGoogle: mockSignInWithGoogle,
    });

    const { getByTestId } = render(<GoogleLoginButton />);
    const loginButton = getByTestId("google-login-button");
    fireEvent.click(loginButton);

    expect(mockSignInWithGoogle).toHaveBeenCalledTimes(0);
  });
});
