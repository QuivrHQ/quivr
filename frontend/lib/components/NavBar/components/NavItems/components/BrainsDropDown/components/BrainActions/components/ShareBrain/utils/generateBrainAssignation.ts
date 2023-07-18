import { BrainRoleAssignation } from "../../../types";

export const generateBrainAssignation = (): BrainRoleAssignation => {
  return {
    email: "",
    rights: "Viewer",
    id: Math.random().toString(),
  };
};
