import { fireEvent, render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import SignUp from "../page";

const mockHandleSignUp = vi.fn(() => ({}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace: vi.fn() }),
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => ({}),
}));

describe("SignUp component", () => {
  it("should render correctly", () => {
    const { getByTestId } = render(<SignUp />);
    const signUpPage = getByTestId("sign-up-page");
    expect(signUpPage).toBeDefined();

    const signUpForm = getByTestId("sign-up-form");
    expect(signUpForm).toBeDefined();

    const emailInput = getByTestId("email-field");
    expect(emailInput).toBeDefined();

    const passwordInput = getByTestId("password-field");
    expect(passwordInput).toBeDefined();

    const signUpButton = getByTestId("sign-up-button");
    expect(signUpButton).toBeDefined();
  });

  it("should correctly fill the email and password fields", () => {
    const { getByTestId } = render(<SignUp />);
    const emailInput = getByTestId("email-field") as HTMLInputElement;
    const passwordInput = getByTestId("password-field") as HTMLInputElement;

    fireEvent.change(emailInput, { target: { value: "user@quivr.app" } });
    fireEvent.change(passwordInput, { target: { value: "password123" } });
    expect(emailInput.value).toBe("user@quivr.app");
    expect(passwordInput.value).toBe("password123");
  });

  it("should call handleSignUp on submit", () => {
    vi.mock("../hooks/useSignUp", async () => {
      const functions = await vi.importActual<
        typeof import("../hooks/useSignUp")
      >("../hooks/useSignUp");

      return {
        useSignUp: () => ({
          ...functions.useSignUp(),
          handleSignUp: () => mockHandleSignUp(),
        }),
      };
    });

    const { getByTestId } = render(<SignUp />);
    const submitForm = getByTestId("sign-up-form") as HTMLFormElement;

    fireEvent.submit(submitForm);
    expect(mockHandleSignUp).toHaveBeenCalled();
  });
});
