import { Locator, Page } from "@playwright/test";

export const getEditor = (page: Page): Locator => {
  const threadInputEditor = page.locator('[data-testid="thread-input"]');
  const contentEditableDiv = threadInputEditor.locator(
    'div[contentEditable="true"]'
  );

  return contentEditableDiv;
};
