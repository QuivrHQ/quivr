import { Page } from "@playwright/test";

export const login = async (page: Page): Promise<void> => {
  const frontendUrl = process.env.NEXT_PUBLIC_E2E_URL;
  const email = process.env.NEXT_PUBLIC_E2E_EMAIL;
  const password = process.env.NEXT_PUBLIC_E2E_PASSWORD;

  if (frontendUrl == null) {
    throw new Error("NEXT_PUBLIC_E2E_URL is not defined");
  }
  if (email == null) {
    throw new Error("NEXT_PUBLIC_E2E_EMAIL is not defined");
  }
  if (password == null) {
    throw new Error("NEXT_PUBLIC_E2E_PASSWORD is not defined");
  }

  await page.goto(frontendUrl);
  await page.getByPlaceholder("Email").click();
  await page.getByPlaceholder("Email").fill("");
  await page.getByPlaceholder("Email").press("Tab");
  await page.getByPlaceholder("Password").fill("");
  await page.getByRole("button", { name: "Login", exact: true }).click();
};
