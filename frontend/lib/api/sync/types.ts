export type Provider = "Google" | "Azure";

export interface Sync {
  name: string;
  provider: Provider;
}
