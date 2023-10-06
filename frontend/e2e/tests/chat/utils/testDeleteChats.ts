import { expect, Page } from "@playwright/test";

export const testDeleteChats = async (page: Page): Promise<void> => {
  const deleteChatButtons = await page.getByTestId("delete-chat-button").all();

  for (const button of deleteChatButtons) {
    await button.click();
  }

  expect((await page.getByTestId("chats-list-item").all()).length === 0);
};
