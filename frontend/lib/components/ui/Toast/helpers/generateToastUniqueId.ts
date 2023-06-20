export const generateToastUniqueId = (): string => {
  const timestamp = Date.now();
  const random = Math.floor(Math.random() * 10000);

  return `${timestamp}-${random}`;
};
