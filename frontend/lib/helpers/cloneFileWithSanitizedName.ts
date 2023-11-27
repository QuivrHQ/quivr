const removeSpecialCharacters = (input: string) =>
  input.normalize("NFD").replace(/[^\w\s.]/g, "");

export const cloneFileWithSanitizedName = (file: File): File => {
  const sanitizedFileName = removeSpecialCharacters(file.name);

  return new File([file], sanitizedFileName, { type: file.type });
};
