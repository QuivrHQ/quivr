const removeDiacriticsFromText = (input: string): string =>
  input.normalize("NFD").replace(/[\u0300-\u036f]/g, "");

export const cloneFileWithSanitizedName = (file: File): File => {
  const sanitizedFileName = removeDiacriticsFromText(file.name);

  return new File([file], sanitizedFileName, { type: file.type });
};
