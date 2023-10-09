import { Locator, Page } from "@playwright/test";

export const getEditor = (page: Page): Locator => {
  const chatInputEditor = page.locator('[data-testid="chat-input"]');
  const contentEditableDiv = chatInputEditor.locator(
    'div[contentEditable="true"]'
  );

  return contentEditableDiv;
};
