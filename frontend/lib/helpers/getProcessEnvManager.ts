// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const getProcessEnvManager = () => {
  const originalEnvValues = { ...process.env };

  const overwriteEnvValuesWith = (values: Record<string, unknown>): void => {
    Object.keys(values).forEach((key) => {
      process.env[key] = values[key] as string;
    });
  };

  const clearEnvValues = (): void => {
    //remove all existing env values
    Object.keys(process.env).forEach((key) => {
      delete process.env[key];
    });
  };

  const resetEnvValues = (): void => {
    clearEnvValues();
    Object.keys(originalEnvValues).forEach((key) => {
      process.env[key] = originalEnvValues[key] as string;
    });
  };

  const getCurrentEnvValues = (): Record<string, unknown> => {
    return { ...process.env };
  };

  return {
    resetEnvValues,
    overwriteEnvValuesWith,
    originalEnvValues,
    getCurrentEnvValues,
  };
};
