import { Page } from "@playwright/test";

export const login = async (page: Page): Promise<void> => {
  const frontendUrl = process.env.NEXT_PUBLIC_E2E_URL;
  const email = process.env.NEXT_PUBLIC_E2E_EMAIL;
  const password = process.env.NEXT_PUBLIC_E2E_PASSWORD;

  if (frontendUrl === undefined) {
    throw new Error("NEXT_PUBLIC_E2E_URL is not defined");
  }
  if (email === undefined) {
    throw new Error("NEXT_PUBLIC_E2E_EMAIL is not defined");
  }
  if (password === undefined) {
    throw new Error("NEXT_PUBLIC_E2E_PASSWORD is not defined");
  }

  await page.goto(frontendUrl);
  await page.getByTestId("login-button").first().click();
  await page.getByPlaceholder("Email").fill(email);
  await page.getByPlaceholder("Password").fill(password);
  await page.getByTestId("submit-login").click();
  await page.getByTestId("chat-page").isVisible();
};
