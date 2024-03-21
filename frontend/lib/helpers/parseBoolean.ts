export const parseBoolean = (value: string | null): boolean => {
  if (value === null) {
    return false;
  }

  return value.toLowerCase() === "true";
};
