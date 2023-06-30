import { render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import Login from "../page";

const mockUseSearchParams = vi.fn(() => ({
  get: vi.fn(),
}));

const mockRedirect = vi.fn((url: string) => ({ url }));

vi.mock("next/navigation", () => ({
  redirect: (url: string) => mockRedirect(url),
  useSearchParams: () => mockUseSearchParams(),
}));

const mockUseSupabase = vi.fn(() => ({
  session: {
    user: {},
  },
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

vi.mock("@/services/analytics/useEventTracking", () => ({
  useEventTracking: () => ({ track: vi.fn() }),
}));

describe("Login component", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("redirects to /upload if user is already signed in and is not coming from another page", () => {
    render(<Login />);
    expect(mockRedirect).toHaveBeenCalledTimes(1);
    expect(mockRedirect).toHaveBeenCalledWith("/upload");
  });

  it('redirects to "/previous-page" if user is already signed in and previous page is set', () => {
    const previousPageUrl = "/my-interesting-page";
    mockUseSearchParams.mockReturnValue({
      get: vi.fn(() => previousPageUrl),
    });
    render(<Login />);
    expect(mockRedirect).toHaveBeenCalledTimes(1);
    expect(mockRedirect).toHaveBeenCalledWith(previousPageUrl);
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
