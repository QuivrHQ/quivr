import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { getProcessEnvManager } from "@/lib/helpers/getProcessEnvManager";

import HomePage from "../page";

const mockUseSupabase = vi.fn(() => ({
  session: {
    user: {},
  },
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

vi.mock("next/navigation", () => ({
  redirect: (url: string) => url,
}));

describe("HomePage", () => {
  it("should render HomePage component properly", () => {
    const { overwriteEnvValuesWith, resetEnvValues } = getProcessEnvManager();

    overwriteEnvValuesWith({
      NEXT_PUBLIC_ENV: "not-local",
    });

    render(<HomePage />);
    const homePage = screen.getByTestId("home-page");
    expect(homePage).toBeDefined();

    resetEnvValues();
  });
});
