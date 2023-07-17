import { BrainRoleType } from "../../../types";

export type SelectOptionsProps = {
  label: string;
  value: BrainRoleType;
};
export const availableRoles: SelectOptionsProps[] = [
  { label: "Viewer", value: "viewer" },
  { label: "Editor", value: "editor" },
];
