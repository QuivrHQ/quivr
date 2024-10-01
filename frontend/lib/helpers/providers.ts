export const transformConnectionLabel = (label: string): string => {
  switch (label) {
    case "Google":
      return "Google Drive";
    case "Azure":
      return "Sharepoint";
    case "DropBox":
      return "Dropbox";
    default:
      return label;
  }
};
