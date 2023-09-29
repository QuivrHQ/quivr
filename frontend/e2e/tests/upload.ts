import { test } from "@playwright/test";

import { login } from "../utils/login";

export const uploadTests = (): void => {
  test("it should be able to add url to crawl", async ({ page }) => {
    await login(page);
    await page.getByTestId("upload-button").click();
    await page.getByTestId("feed-card").isVisible();
    await page.getByTestId("urlToCrawlInput").click();
    await page.getByTestId("urlToCrawlInput").fill("https://quivr.app");
    await page.getByTestId("urlToCrawlInput").press("Enter");
    await page.getByTestId("urlToCrawlInput").fill("https://google.fr");
    await page.getByTestId("urlToCrawlInputSubmit").click();
    await page.getByTestId("submit-feed-button").click();
    await page.getByTestId("feed-card").isHidden();
  });
};
