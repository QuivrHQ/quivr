import { BrainRoleAssignation } from "../../NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";

export const generateBrainAssignation = (): BrainRoleAssignation => {
  return {
    email: "",
    role: "Viewer",
    id: Math.random().toString(),
  };
};
