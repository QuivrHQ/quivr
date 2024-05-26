export type Provider = "Google" | "Azure";

export interface SyncElement {
  name: string;
  id: string;
  is_folder: boolean;
}

interface Credentials {
  token: string;
}
export interface Sync {
  name: string;
  provider: Provider;
  id: number;
  credentials: Credentials;
}
