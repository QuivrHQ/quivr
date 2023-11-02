export const supportedFileExtensions = [
  "txt",
  "csv",
  "md",
  "markdown",
  "m4a",
  "mp3",
  "mpga",
  "mpeg",
  "webm",
  "mp4",
  "wav",
  "pdf",
  "html",
  "pptx",
  "docx",
  "odt",
  "xlsx",
  "xls",
  "epub",
  "ipynb",
  "py",
  "telegram",
] as const;

export type SupportedFileExtensions = (typeof supportedFileExtensions)[number];

export type SupportedFileExtensionsWithDot = `.${SupportedFileExtensions}`;
