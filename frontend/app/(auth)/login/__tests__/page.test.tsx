import { render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import Login from "../page";

const mockRedirect = vi.fn((url: string) => ({ url }));

vi.mock("next/navigation", () => ({
  redirect: (url: string) => mockRedirect(url),
}));

const mockUseSupabase = vi.fn(() => ({
  session: {
    user: {},
  },
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

vi.mock("@/services/analytics/june/useEventTracking", () => ({
  useEventTracking: () => ({ track: vi.fn() }),
}));

describe("Login component", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("redirects to /upload if user is already signed in and is not coming from another page", () => {
    render(<Login />);
    expect(mockRedirect).toHaveBeenCalledTimes(1);
    expect(mockRedirect).toHaveBeenCalledWith("/chat");
  });

  it('redirects to "/previous-page" if user is already signed in and previous page is set', () => {
    const currentPage = "/my-awesome-page";

    Object.defineProperty(window, "location", {
      value: { pathname: currentPage },
    });

    const sessionStorageData: Record<string, string> = {
      "previous-page": currentPage,
    };

    const sessionStorageMock = {
      getItem: vi.fn((key: string) => sessionStorageData[key]),
      setItem: vi.fn(
        (key: string, value: string) => (sessionStorageData[key] = value)
      ),
      removeItem: vi.fn((key: string) => delete sessionStorageData[key]),
    };

    Object.defineProperty(window, "sessionStorage", {
      value: sessionStorageMock,
    });

    render(<Login />);
    expect(mockRedirect).toHaveBeenCalledTimes(1);
    expect(mockRedirect).toHaveBeenCalledWith(currentPage);
  });

  it("should render the login form when user is not signed in", () => {
    mockUseSupabase.mockReturnValue({
      //@ts-expect-error doing this for testing purposes
      session: { user: undefined },
    });
    const { getByTestId } = render(<Login />);
    const signInForm = getByTestId("sign-in-form");
    expect(signInForm).toBeDefined();
  });
});
