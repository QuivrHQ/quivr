import { BrainRoleAssignation } from "../../BrainUsers/types";

export const generateBrainAssignation = (): BrainRoleAssignation => {
  return {
    email: "",
    role: "Viewer",
    id: Math.random().toString(),
  };
};
