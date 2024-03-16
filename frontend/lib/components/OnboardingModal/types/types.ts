import { CompanySize } from "@/lib/api/user/user";

export type OnboardingProps = {
  username: string;
  companyName: string;
  companySize: CompanySize;
  usagePurpose: string;
};
