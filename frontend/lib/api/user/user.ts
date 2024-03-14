import { AxiosInstance } from "axios";
import { UUID } from "crypto";

import { UserStats } from "@/lib/types/User";

export enum CompanySize {
  One = "1-10",
  Two = "10-25",
  Three = "25-50",
  Four = "50-100",
  Five = "100-500",
  Six = "500-1000",
  Seven = "1000-5000",
  Eight = "+5000",
}

export enum CompanyRole {
  accountExecutive = "Account Executive",
  accountant = "Accountant",
  businessAnalyst = "Business Analyst",
  businessDevelopmentManager = "Business Development Manager",
  chiefExecutiveOfficer = "Chief Executive Officer",
  chiefFinancialOfficer = "Chief Financial Officer",
  chiefInformationOfficer = "Chief Information Officer",
  chiefMarketingOfficer = "Chief Marketing Officer",
  chiefOperatingOfficer = "Chief Operating Officer",
  chiefPeopleOfficer = "Chief People Officer",
  chiefTechnologyOfficer = "Chief Technology Officer",
  communicationsManager = "Communications Manager",
  contentCreator = "Content Creator",
  customerRelationshipManager = "Customer Relationship Manager",
  customerServiceRepresentative = "Customer Service Representative",
  dataAnalyst = "Data Analyst",
  dataEngineer = "Data Engineer",
  dataScientist = "Data Scientist",
  developer = "Developer",
  digitalMarketingSpecialist = "Digital Marketing Specialist",
  directorOfEngineering = "Director Of Engineering",
  environmentalHealthAndSafetyOfficer = "Environmental Health And Safety Officer",
  financeManager = "Finance Manager",
  frontEndDeveloper = "Front End Developer",
  graphicDesigner = "Graphic Designer",
  humanResourcesCoordinator = "Human Resources Coordinator",
  humanResourcesManager = "Human Resources Manager",
  informationSecurityAnalyst = "Information Security Analyst",
  itSupportSpecialist = "IT Support Specialist",
  legalAdvisor = "Legal Advisor",
  logisticsCoordinator = "Logistics Coordinator",
  marketingCoordinator = "Marketing Coordinator",
  marketingManager = "Marketing Manager",
  networkAdministrator = "Network Administrator",
  officeManager = "Office Manager",
  operationsManager = "Operations Manager",
  productDesigner = "Product Designer",
  productManager = "Product Manager",
  projectCoordinator = "Project Coordinator",
  projectManager = "Project Manager",
  publicRelationsSpecialist = "Public Relations Specialist",
  qualityAssuranceEngineer = "Quality Assurance Engineer",
  recruitmentSpecialist = "Recruitment Specialist",
  salesAssociate = "Sales Associate",
  salesManager = "Sales Manager",
  scrumMaster = "Scrum Master",
  socialMediaManager = "Social Media Manager",
  softwareArchitect = "Software Architect",
  softwareDeveloper = "Software Developer",
  softwareEngineer = "Software Engineer",
  solutionsArchitect = "Solutions Architect",
  supplyChainManager = "Supply Chain Manager",
  supportSpecialist = "Support Specialist",
  systemAdministrator = "System Administrator",
  technicalLead = "Technical Lead",
  technicalSupportSpecialist = "Technical Support Specialist",
  uiUxDesigner = "UI/UX Designer",
  webDesigner = "Web Designer",
  webDeveloper = "Web Developer",
}

export type UserIdentityUpdatableProperties = {
  username: string;
  company?: string;
  onboarded: boolean;
  company_size?: CompanySize;
  role_in_company?: CompanyRole;
};

export type UserIdentity = {
  user_id: UUID;
  onboarded: boolean;
  username: string;
};

export const updateUserIdentity = async (
  userUpdatableProperties: UserIdentityUpdatableProperties,
  axiosInstance: AxiosInstance
): Promise<UserIdentity> =>
  axiosInstance.put(`/user/identity`, userUpdatableProperties);

export const getUserIdentity = async (
  axiosInstance: AxiosInstance
): Promise<UserIdentity> => {
  const { data } = await axiosInstance.get<UserIdentity>(`/user/identity`);

  return data;
};

export const getUser = async (
  axiosInstance: AxiosInstance
): Promise<UserStats> => (await axiosInstance.get<UserStats>("/user")).data;
