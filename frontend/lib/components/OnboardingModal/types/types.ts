export enum UserDiscoverySource {
  Twitter = "Twitter",
  LinkedIn = "Linkedin",
  Github = "Github",
  SEO = "SEO",
  Other = "Other",
}

export type OnboardingProps = {
  username: string;
  companyName: string;
  discoverySource: UserDiscoverySource;
};
