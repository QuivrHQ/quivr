import { Page } from "@playwright/test";

import { getEditor } from "./getEditor";

export const testSelectBrain = async (page: Page): Promise<void> => {
  const randomMessage = Math.random().toString(36).substring(7);

  const editor = getEditor(page);

  await editor.fill("@");

  await page.getByText("Test brain").first().click();

  await editor.fill(randomMessage);

  await page.getByTestId("submit-button").click();

  await page
    .getByTestId("chat-message-text")
    .getByText(`${randomMessage}`)
    .isVisible();

  await page.getByTestId("brain-tags").getByText("Test brain").isVisible();
};
