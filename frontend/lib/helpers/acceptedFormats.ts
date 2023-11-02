import { SupportedFileExtensionsWithDot } from "@/lib/types/SupportedFileExtensions";

export const acceptedFormats: Record<string, SupportedFileExtensionsWithDot[]> =
  {
    "text/plain": [".txt"],
    "text/csv": [".csv"],
    "text/markdown": [".md", ".markdown"],
    "audio/x-m4a": [".m4a"],
    "audio/mpeg": [".mp3", ".mpga", ".mpeg"],
    "audio/webm": [".webm"],
    "video/mp4": [".mp4"],
    "audio/wav": [".wav"],
    "application/pdf": [".pdf"],
    "text/html": [".html"],
    "text/telegram": [".telegram"],

    "application/vnd.openxmlformats-officedocument.presentationml.presentation":
      [".pptx"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [
      ".docx",
    ],
    "application/vnd.oasis.opendocument.text": [".odt"],
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
      ".xlsx",
      ".xls",
    ],
    "application/epub+zip": [".epub"],
    "application/x-ipynb+json": [".ipynb"],
    "text/x-python": [".py"],
  };
