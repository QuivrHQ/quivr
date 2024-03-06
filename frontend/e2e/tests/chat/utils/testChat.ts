import { Page } from "@playwright/test";

import { getEditor } from "./getEditor";

export const testThread = async (page: Page): Promise<void> => {
  const randomMessage = Math.random().toString(36).substring(7);

  const editor = getEditor(page);

  await editor.fill(randomMessage);

  await page.getByTestId("submit-button").click();

  await page
    .getByTestId("thread-message-text")
    .getByText(`${randomMessage}`)
    .isVisible();
};
