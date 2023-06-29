import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { getProcessEnvManager } from "@/lib/helpers/getProcessEnvManager";

import HomePage from "../page";

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
