import { RedirectType } from "next/dist/client/components/redirect";
import { describe, expect, it, vi } from "vitest";

import { redirectToLogin } from "../redirectToLogin";

const currentPage = "/my-awesome-page";

const redirectMock = vi.fn((...params: unknown[]) => ({ params }));

vi.mock("next/navigation", () => ({
  redirect: (...params: unknown[]) => redirectMock(...params),
}));

const sessionStorageData: Record<string, string> = {};

const sessionStorageMock = {
  getItem: vi.fn((key: string) => sessionStorageData[key]),
  setItem: vi.fn(
    (key: string, value: string) => (sessionStorageData[key] = value)
  ),
};

Object.defineProperty(window, "sessionStorage", {
  value: sessionStorageMock,
});
Object.defineProperty(window, "location", {
  value: { pathname: currentPage },
});

describe("redirectToLogin", () => {
  it("should save previous page before redirection", () => {
    redirectToLogin(RedirectType.push);
    expect(sessionStorage.getItem("previous-page")).toBe(currentPage);
    expect(redirectMock).toHaveBeenCalledTimes(1);
    expect(redirectMock).toHaveBeenCalledWith("/login", RedirectType.push);
  });
});
