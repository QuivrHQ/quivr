import { Page } from "@playwright/test";

import { getEditor } from "./getEditor";

export const testUnplugChat = async (page: Page): Promise<void> => {
  await page.getByTestId("remove-mention").click();
  await page.getByTestId("mention-input").isHidden();

  const randomMessage = Math.random().toString(36).substring(7);

  const editor = getEditor(page);

  await editor.fill(randomMessage);

  await page.getByTestId("submit-button").click();

  await page
    .getByTestId("chat-message-text")
    .getByText(`${randomMessage}`)
    .isVisible();
};
