export const getNonEmptyValuesFromDict = (
  values: Record<string, string>
): Record<string, string> => {
  const nonEmptyValues = Object.entries(values).reduce((acc, [key, value]) => {
    if (value !== "") {
      acc[key] = value;
    }

    return acc;
  }, {} as Record<string, string>);

  return nonEmptyValues;
};
