import { test } from "@playwright/test";

import { testChat } from "./utils/testChat";

export const chatTests = (): void => {
  test("chat", async ({ page }) => {
    await login(page);
    await testChat(page);
  });
};
