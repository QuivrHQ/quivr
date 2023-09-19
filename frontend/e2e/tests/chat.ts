import { test } from "@playwright/test";

import { login } from "../utils/login";

export const chatTests = (): void => {
  test("chat", async ({ page }) => {
    await login(page);
    await page.goto("/chat");
    await page.getByRole("combobox").locator("div").nth(2).click();
    await page.getByRole("combobox").fill("Hello");
    await page.getByTestId("submit-button").click();
  });
};
