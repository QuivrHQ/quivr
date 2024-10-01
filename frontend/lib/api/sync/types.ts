import { UUID } from "crypto";

export type Provider = "Google" | "Azure" | "DropBox" | "Notion" | "GitHub";

export type Integration =
  | "Google Drive"
  | "Share Point"
  | "Dropbox"
  | "Notion"
  | "GitHub";

export type SyncStatus = "SYNCING" | "SYNCED" | "ERROR" | "REMOVED";

export interface KMSElement {
  id: UUID;
  file_name?: string;
  sync_file_id: string | null;
  is_folder: boolean;
  icon?: string;
  sync_id: number | null;
  parentKMSElement?: KMSElement;
}

interface Credentials {
  token: string;
}

export interface Sync {
  name: string;
  provider: Provider;
  id: number;
  credentials: Credentials;
  email: string;
  status: SyncStatus;
}

export interface SyncsByProvider {
  provider: Provider;
  syncs: Sync[];
}

export interface SyncSettings {
  folders?: string[];
  files?: string[];
}

export interface ActiveSync {
  id: number;
  name: string;
  syncs_user_id: number;
  user_id: string;
  settings: SyncSettings;
  last_synced: string;
  sync_interval_minutes: number;
  brain_id: string;
  syncs_user: {
    provider: Provider;
  };
}

export interface OpenedConnection {
  user_sync_id: number;
  id: number | undefined;
  provider: Provider;
  submitted: boolean;
  selectedFiles: KMSElement[];
  name: string;
  last_synced: string;
  cleaned?: boolean;
}
