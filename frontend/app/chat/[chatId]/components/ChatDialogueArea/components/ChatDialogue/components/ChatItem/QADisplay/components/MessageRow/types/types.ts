export interface CitationType {
  citation: string;
  filename: string;
  file_url: string;
}

export interface SourceFile {
  filename: string;
  file_url: string;
  citations: string[];
}
