export const setEmptyStringsUndefined = (
  obj: Record<string, unknown>
): Record<string, unknown> => {
  Object.keys(obj).forEach((key) => {
    if (obj[key] === "") {
      obj[key] = undefined;
    }
  });

  return obj;
};
