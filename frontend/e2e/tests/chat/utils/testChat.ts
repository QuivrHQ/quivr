import { Page } from "@playwright/test";

import { getEditor } from "./getEditor";

export const testChat = async (page: Page): Promise<void> => {
  const randomMessage = Math.random().toString(36).substring(7);

  const editor = getEditor(page);

  await editor.fill(randomMessage);

  await page.getByTestId("submit-button").click();

  await page
    .getByTestId("chat-message-text")
    .getByText(`${randomMessage}`)
    .isVisible();
};
