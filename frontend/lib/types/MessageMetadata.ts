export interface CloseBrain {
  id: string;
  similarity: number;
  name: string;
}

export interface MessageMetadata {
  closeBrains: CloseBrain[];
}
