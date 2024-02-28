import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { MdOutlineRemoveCircle } from "react-icons/md";

import Field from "@/lib/components/ui/Field";

import { SingleSelector } from "./ui/SingleSelector/SingleSelector";

import {
  BrainRoleAssignation,
  BrainRoleType,
  userRoleToAssignableRoles,
} from "../../app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/types";

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
  const { t } = useTranslation("translation");
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>(
    roleAssignation.role
  );
  const [email, setEmail] = useState(roleAssignation.email);

  useEffect(() => {
    if (
      email !== roleAssignation.email ||
      selectedRole !== roleAssignation.role
    ) {
      onChange({
        ...roleAssignation,
        email,
        role: selectedRole,
      });
    }
  }, [email, onChange, roleAssignation, selectedRole]);

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
          placeholder={t("email")}
          onChange={(e) => setEmail(e.target.value)}
          value={email}
          onBlur={() => email === "" && removeCurrentInvitation?.()}
          data-testid="role-assignation-email-input"
        />
      </div>

      <SingleSelector
        selectedOption={{ label: selectedRole, value: selectedRole }}
        options={userRoleToAssignableRoles["Owner"]}
        onChange={setSelectedRole}
        placeholder="Role"
        iconName="user"
      />
    </div>
  );
};
