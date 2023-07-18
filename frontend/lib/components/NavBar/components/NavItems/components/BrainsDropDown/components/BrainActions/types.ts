export const roles = ["Viewer", "Editor", "Owner"] as const;

export type BrainRoleType = (typeof roles)[number];

export type BrainRoleAssignation = {
  email: string;
  rights: BrainRoleType;
  id: string;
};
