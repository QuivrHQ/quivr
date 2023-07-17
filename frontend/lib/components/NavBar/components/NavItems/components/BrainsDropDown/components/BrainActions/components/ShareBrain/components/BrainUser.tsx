import { useState } from "react";
import { MdOutlineRemoveCircle } from "react-icons/md";

import Field from "@/lib/components/ui/Field";
import { Select } from "@/lib/components/ui/Select";

import { BrainRoleType } from "../../../types";
import { availableRoles } from "../types";

type BrainUserProps = {
  email: string;
  rights: BrainRoleType;
};

export const BrainUser = ({
  email,
  rights: role,
}: BrainUserProps): JSX.Element => {
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>(role);

  const updateSelectedRole = (newRole: BrainRoleType) => {
    setSelectedRole(newRole);
  };

  const removeCurrentInvitation = () => {
    alert("soon");
  };

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
          value={email}
          data-testid="role-assignation-email-input"
          readOnly
        />
      </div>
      <Select
        onChange={updateSelectedRole}
        value={selectedRole}
        options={availableRoles}
      />
    </div>
  );
};
