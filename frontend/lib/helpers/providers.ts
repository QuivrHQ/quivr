export const transformConnectionLabel = (label: string): string => {
  switch (label.toLowerCase()) {
    case "google":
      return "Google Drive";
    case "azure":
      return "Sharepoint";
    case "dropbox":
      return "Dropbox";
    default:
      return label;
  }
};
