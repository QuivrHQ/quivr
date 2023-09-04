export const isValidUrl = (string: string): boolean => {
  try {
    new URL(string);

    return true;
  } catch (_) {
    return false;
  }
};
