import { describe, expect, it } from "vitest";

import { getProcessEnvManager } from "../getProcessEnvManager";

describe("getEnvManager", () => {
  it("should overwrite environment values", () => {
    process.env.MY_VALUE = "test value";
    const processEnvManager = getProcessEnvManager();

    processEnvManager.overwriteEnvValuesWith({ MY_VALUE: "new value" });

    expect(process.env.MY_VALUE).toBe("new value");
  });

  it("should reset environment values", () => {
    //@ts-expect-error doing this for testing purposes
    process.env = {
      TEST_ENV: "test value",
    };
    const { resetEnvValues, originalEnvValues, getCurrentEnvValues } =
      getProcessEnvManager();

    process.env.TEST_ENV = "test value overwritten";
    resetEnvValues();

    expect(originalEnvValues).toEqual(getCurrentEnvValues());
  });

  it("should return a copy of the current environment values", () => {
    process.env.TEST_ENV = "test value";
    const { getCurrentEnvValues } = getProcessEnvManager();
    const envValues = getCurrentEnvValues();
    expect(envValues).toEqual({ ...process.env, TEST_ENV: "test value" });
  });

  it("should return the copy of original environment values", () => {
    const initEnvValues = {
      TEST_ENV_1: "test value",
      TEST_ENV_2: "test value2",
    };
    //@ts-expect-error doing this for testing purposes
    process.env = { ...initEnvValues };

    const { originalEnvValues } = getProcessEnvManager();

    process.env.TEST_ENV_1 = "test value overwritten";

    expect(originalEnvValues).toEqual(initEnvValues);
  });
});
