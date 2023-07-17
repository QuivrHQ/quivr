import { BrainRoleAssignation } from "../../../types";

export const generateBrainAssignation = (): BrainRoleAssignation => {
  return {
    email: "",
    rights: "viewer",
    id: Math.random().toString(),
  };
};
