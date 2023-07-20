import { BrainRoleAssignation } from "../../../types";

export const generateBrainAssignation = (): BrainRoleAssignation => {
  return {
    email: "",
    role: "Viewer",
    id: Math.random().toString(),
  };
};
