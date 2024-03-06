import { test } from "@playwright/test";

import { testDeleteThreads } from "./utils/testDeleteThreads";
import { testSelectBrain } from "./utils/testSelectBrain";
import { testThread } from "./utils/testThread";
import { testUnplugThread } from "./utils/testUnplugThread";

import { login } from "../../utils/login";

export const threadTests = (): void => {
  test("thread", async ({ page }) => {
    await login(page);
    await testThread(page);
    await testUnplugThread(page);
    await testSelectBrain(page);
    await testDeleteThreads(page);
  });
};
