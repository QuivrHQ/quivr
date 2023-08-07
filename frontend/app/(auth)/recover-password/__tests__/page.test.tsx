/* eslint-disable max-lines */
import { fireEvent, render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import RecoverPassword from "../page";

const mockUsePathname = vi.fn(() => "/previous-page");
const mockRedirect = vi.fn((url: string) => ({ url }));

vi.mock("next/navigation", () => ({
  redirect: (url: string) => mockRedirect(url),
  usePathname: () => mockUsePathname(),
}));

const mockUseSupabase = vi.fn(() => ({
  supabase: {
    auth: {
      updateUser: vi.fn(),
    },
  },
  session: {
    user: {},
  },
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

const mockPublish = vi.fn();

vi.mock("@/lib/hooks/useToast", () => ({
  useToast: () => ({
    publish: mockPublish,
  }),
}));

const mockTrack = vi.fn();

vi.mock("@/services/analytics/useEventTracking", () => ({
  useEventTracking: () => ({
    track: mockTrack,
  }),
}));

describe("RecoverPassword component", () => {
  it("should render the password update form", () => {
    mockUseSupabase.mockReturnValue({
      //@ts-expect-error doing this for testing purposes
      session: { user: undefined },
    });
    const { getByTestId } = render(<RecoverPassword />);
    const passwordField = getByTestId("password-field");
    const updateButton = getByTestId("update-button");

    expect(passwordField).toBeDefined();
    expect(updateButton).toBeDefined();
  });

  it.skip("should update the password and shows success toast", async () => {
    const updateUserMock = vi.fn(() => ({
      data: {},
    }));
    mockUseSupabase.mockReturnValue({
      supabase: {
        auth: {
          updateUser: updateUserMock,
        },
      },
      session: { user: {} },
    });
    const { getByTestId } = render(<RecoverPassword />);
    const passwordField = getByTestId("password-field");
    const updateButton = getByTestId("update-button");

    const newPassword = "new-password";
    fireEvent.change(passwordField, { target: { value: newPassword } });
    fireEvent.click(updateButton);

    expect(mockTrack).toHaveBeenCalledTimes(1);
    expect(mockTrack).toHaveBeenCalledWith("UPDATE_PASSWORD");

    return new Promise<void>((resolve) => {
      setTimeout(() => {
        expect(mockPublish).toHaveBeenCalledTimes(1);
        expect(mockPublish).toHaveBeenCalledWith({
          variant: "success",
          text: "Password updated successfully!",
        });
        expect(updateUserMock).toHaveBeenCalledTimes(1);
        expect(updateUserMock).toHaveBeenCalledWith({
          password: newPassword,
        });
        resolve();
      }, 0);
    });
  });

  it.skip("should show error toast when password update fails", async () => {
    const errorMessage = "Password update failed";
    const updateUserMock = vi.fn(() => ({
      error: { message: errorMessage },
    }));
    mockUseSupabase.mockReturnValue({
      supabase: {
        auth: {
          updateUser: updateUserMock,
        },
      },
      session: { user: {} },
    });
    const { getByTestId } = render(<RecoverPassword />);
    const passwordField = getByTestId("password-field");
    const updateButton = getByTestId("update-button");

    fireEvent.change(passwordField, { target: { value: "new-password" } });
    fireEvent.click(updateButton);

    expect(mockPublish).toHaveBeenCalledTimes(1);

    return new Promise<void>((resolve) => {
      setTimeout(() => {
        expect(mockPublish).toHaveBeenCalledWith({
          variant: "danger",
          text: `Error: ${errorMessage}`,
        });
        resolve();
      }, 0);
    });
  });
});
