import { useEffect, useState } from "react";
import { MdOutlineRemoveCircle } from "react-icons/md";

import Field from "@/lib/components/ui/Field";
import { Select } from "@/lib/components/ui/Select";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainRoleAssignation, BrainRoleType } from "../../../types";
import { userRoleToAssignableRoles } from "../types";

type UserToInviteProps = {
  onChange: (newRole: BrainRoleAssignation) => void;
  removeCurrentInvitation?: () => void;
  roleAssignation: BrainRoleAssignation;
};

export const UserToInvite = ({
  onChange,
  removeCurrentInvitation,
  roleAssignation,
}: UserToInviteProps): JSX.Element => {
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>(
    roleAssignation.rights
  );
  const [email, setEmail] = useState(roleAssignation.email);
  const { currentBrain } = useBrainContext();

  if (currentBrain === undefined) {
    throw new Error("Brain is undefined");
  }

  useEffect(() => {
    onChange({
      ...roleAssignation,
      email,
      rights: selectedRole,
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
        options={userRoleToAssignableRoles[currentBrain.rights]}
      />
    </div>
  );
};
