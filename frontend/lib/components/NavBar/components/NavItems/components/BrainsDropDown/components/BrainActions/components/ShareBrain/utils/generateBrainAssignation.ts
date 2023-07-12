import { BrainRoleAssignation } from "../../../types";

export const generateBrainAssignation = (): BrainRoleAssignation => {
  return {
    email: "",
    role: "viewer",
    id: Math.random().toString(),
  };
};
