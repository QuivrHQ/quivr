import { defineConfig, devices } from "@playwright/test";
import dotenv from "dotenv";
dotenv.config();
export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !(process.env.CI == null),
  retries: process.env.CI != null ? 2 : 0,
  workers: 1,
  reporter: "html",
  testMatch: "e2e/index.ts",
  use: {
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: {
    command:
      process.env.NODE_ENV === "production"
        ? "yarn run build && yarn run start -p 3003"
        : "yarn run dev -p 3003",
    url: process.env.NEXT_PUBLIC_E2E_URL,
  },
});
