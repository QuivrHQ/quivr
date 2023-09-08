import { test } from "@playwright/test";

import { login } from "./utils/login";

test("create brain", async ({ page }) => {
  await login(page);
  await page.goto("/user");
  await page.getByLabel("Settings").click();
  await page.getByLabel("Hide Errors").click();
  await page.getByRole("button", { name: "Add New Brain" }).click();
  await page
    .getByRole("textbox", { name: "E.g. History notes" })
    .fill("Test brain");
  await page.getByRole("button", { name: "Create" }).click();
});
