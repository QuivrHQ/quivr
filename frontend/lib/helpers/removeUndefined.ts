export const removeUndefined = <T extends Record<string, unknown>>(
  obj: T
): Partial<T> => {
  const newObj = {} as Partial<T>;
  for (const key in obj) {
    if (obj[key] !== undefined) {
      newObj[key] = obj[key];
    }
  }

  return newObj;
};
