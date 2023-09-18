import { test } from "@playwright/test";

import { login } from "../utils/login";

export const uploadTests = (): void => {
  test("upload", async ({ page }) => {
    await login(page);
    await page.goto("/chat");
    await page.getByTestId("upload-button").click();
    await page
      .getByRole("button", {
        name: "Drag and drop files here, or click to browse",
      })
      .click();
    await page.getByPlaceholder("Insert website URL").click();
    await page.getByPlaceholder("Insert website URL").fill("https://quivr.app");
    await page.getByPlaceholder("Insert website URL").press("Enter");
  });
};
