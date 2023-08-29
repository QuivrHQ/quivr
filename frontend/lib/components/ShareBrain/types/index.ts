import { BrainRoleType } from "../../BrainUsers/types";

export type SelectOptionsProps = {
  label: string;
  value: BrainRoleType;
};
export const availableRoles: SelectOptionsProps[] = [
  { label: "Viewer", value: "Viewer" },
  { label: "Editor", value: "Editor" },
  { label: "Owner", value: "Owner" },
];

export const userRoleToAssignableRoles: Record<
  BrainRoleType,
  SelectOptionsProps[]
> = {
  Viewer: [],
  Editor: [
    { label: "Viewer", value: "Viewer" },
    { label: "Editor", value: "Editor" },
  ],

  Owner: [
    { label: "Viewer", value: "Viewer" },
    { label: "Editor", value: "Editor" },
    { label: "Owner", value: "Owner" },
  ],
};
