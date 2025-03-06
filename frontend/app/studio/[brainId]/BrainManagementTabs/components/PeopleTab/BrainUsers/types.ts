export const roles = ["Viewer", "Editor", "Owner"] as const;

export type BrainRoleType = (typeof roles)[number];

export type BrainRoleAssignation = {
  email: string;
  role: BrainRoleType;
  id: string;
};

export type SelectOptionsProps = {
  label: string;
  value: BrainRoleType;
};
export const availableRoles: SelectOptionsProps[] = [
  { label: "Người xem", value: "Viewer" },
  { label: "Người chỉnh sửa", value: "Editor" },
  { label: "Người sở hữu", value: "Owner" },
];

export const userRoleToAssignableRoles: Record<
  BrainRoleType,
  SelectOptionsProps[]
> = {
  Viewer: [],
  Editor: [
    { label: "Người xem", value: "Viewer" },
    { label: "Người chỉnh sửa", value: "Editor" },
  ],

  Owner: [
    { label: "Người xem", value: "Viewer" },
    { label: "Người chỉnh sửa", value: "Editor" },
    { label: "Người sở hữu", value: "Owner" },
  ],
};
