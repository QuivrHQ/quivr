export interface CloseBrain {
  id: string;
  similarity: number;
  name: string;
}

export interface Source {
  frequency: number;
  name: string;
  source_url: string;
  type: string;
}

export interface MessageMetadata {
  closeBrains: CloseBrain[];
  sources: Source[];
}
