export const roles = ["Viewer", "Editor", "Owner"] as const;

export type BrainRoleType = (typeof roles)[number];

export type BrainRoleAssignation = {
  email: string;
  role: BrainRoleType;
  id: string;
};
