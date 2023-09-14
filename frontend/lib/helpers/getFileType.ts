import {
  SupportedFileExtensions,
  supportedFileExtensions,
} from "../types/SupportedFileExtensions";

export const getFileType = (
  fileName: string
): SupportedFileExtensions | undefined => {
  const extension = fileName.split(".").pop()?.toLowerCase() ?? "";
  if (supportedFileExtensions.includes(extension as SupportedFileExtensions)) {
    return extension as SupportedFileExtensions;
  }

  return undefined;
};
