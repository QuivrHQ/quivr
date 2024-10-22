import { UUID } from "crypto";

export interface AddFolderData {
  parent_id: UUID | null;
  file_name: string;
  is_folder: boolean;
}

export interface AddKnowledgeFileData {
  parent_id: UUID | null;
  file_name: string;
  is_folder: boolean;
}

export interface AddKnowledgeUrlData {
  parent_id: UUID | null;
  is_folder: boolean;
  url: string;
}
