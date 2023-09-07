export const removeFileExtension = (fileName: string): string => {
  const lastDotIndex = fileName.lastIndexOf(".");
  if (lastDotIndex !== -1) {
    return fileName.substring(0, lastDotIndex);
  }

  return fileName;
};
