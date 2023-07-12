import { useEffect, useState } from "react";
import { MdOutlineRemoveCircle } from "react-icons/md";

import Field from "@/lib/components/ui/Field";
import { Select } from "@/lib/components/ui/Select";

import { BrainRoleAssignation, BrainRoleType } from "../../../types";

type AddUserRowProps = {
  onChange: (newRole: BrainRoleAssignation) => void;
  removeCurrentInvitation?: () => void;
  roleAssignation: BrainRoleAssignation;
};

type SelectOptionsProps = {
  label: string;
  value: BrainRoleType;
};
const SelectOptions: SelectOptionsProps[] = [
  { label: "Viewer", value: "viewer" },
  { label: "Editor", value: "editor" },
];

export const InvitedUserRow = ({
  onChange,
  removeCurrentInvitation,
  roleAssignation,
}: AddUserRowProps): JSX.Element => {
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>(
    roleAssignation.role
  );
  const [email, setEmail] = useState(roleAssignation.email);

  useEffect(() => {
    onChange({
      ...roleAssignation,
      email,
      role: selectedRole,
    });
  }, [email, selectedRole]);

  return (
    <div
      data-testid="assignation-row"
      className="flex flex-row align-center my-2 gap-3 items-center"
    >
      <div className="cursor-pointer" onClick={removeCurrentInvitation}>
        <MdOutlineRemoveCircle />
      </div>
      <div className="flex flex-1">
        <Field
          name="email"
          required
          type="email"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
          value={email}
          onBlur={() => email === "" && removeCurrentInvitation?.()}
          data-testid="role-assignation-email-input"
        />
      </div>
      <Select
        onChange={setSelectedRole}
        value={selectedRole}
        options={SelectOptions}
      />
    </div>
  );
};
