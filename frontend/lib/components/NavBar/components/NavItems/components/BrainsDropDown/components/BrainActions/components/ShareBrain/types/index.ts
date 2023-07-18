import { BrainRoleType } from "../../../types";

export type SelectOptionsProps = {
  label: string;
  value: BrainRoleType;
};
export const availableRoles: SelectOptionsProps[] = [
  { label: "Viewer", value: "Viewer" },
  { label: "Editor", value: "Editor" },
  { label: "Owner", value: "Owner" },
];
