export const roles = ["Viewer", "Editor", "Owner"] as const;

//TODO: move these types to a shared place
export type BrainRoleType = (typeof roles)[number];

export type BrainRoleAssignation = {
  email: string;
  role: BrainRoleType;
  id: string;
};
