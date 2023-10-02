import { test } from "@playwright/test";

import { login } from "../utils/login";

export const createBrainTests = (): void => {
  test("create brain", async ({ page }) => {
    await login(page);
    await page.getByTestId("brain-management-button").click();
    await page.getByTestId("add-brain-button").click();
    await page.getByTestId("brain-name").fill("Test brain");
    await page.getByTestId("create-brain-submit-button").click();
  });
};
