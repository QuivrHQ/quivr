export const roles = ["viewer", "editor"];

export type BrainRoleType = (typeof roles)[number];

export type BrainRoleAssignation = {
  email: string;
  role: BrainRoleType;
  id: string;
};
