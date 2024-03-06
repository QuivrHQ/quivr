import { expect, Page } from "@playwright/test";

export const testDeleteThreads = async (page: Page): Promise<void> => {
  const deleteThreadButtons = await page
    .getByTestId("delete-thread-button")
    .all();

  for (const button of deleteThreadButtons) {
    await button.click();
  }

  expect((await page.getByTestId("threads-list-item").all()).length === 0);
};
