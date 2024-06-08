export type Provider = "Google" | "Azure";

export interface SyncElement {
  name?: string;
  id: string;
  is_folder: boolean;
}

export interface SyncElements {
  files: SyncElement[];
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
  selectedFiles: SyncElements;
  name: string;
  last_synced: string;
  cleaned?: boolean;
}
