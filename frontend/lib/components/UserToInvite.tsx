import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { Select } from "@/lib/components/ui/Select";

import { BrainRoleType } from "./BrainUsers/types";
import { userRoleToAssignableRoles } from "./ShareBrain/types";
import { TextInput } from "./ui/TextInput/TextInput";

import { useShareBrain } from "../hooks/useShareBrain";

export const UserToInvite = (brainId: { brainId: string }): JSX.Element => {
  const { t } = useTranslation("translation");
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>("Viewer");
  const [email, setEmail] = useState("");
  const { updateRoleAssignation } = useShareBrain(brainId.brainId);

  const assignableRoles = userRoleToAssignableRoles["Owner"];
  const translatedOptions = assignableRoles.map((role) => ({
    value: role.value,
    label: t(role.value),
  }));

  useEffect(() => {
    console.info(email);
  }, [email]);

  const handleUpdateRoleAssignation = (): void => {
    console.info("hey");
  };

  return (
    <div className="flex flex-row align-center my-2 gap-3 items-center">
      <TextInput
        label="Email"
        inputValue={email}
        setInputValue={setEmail}
        onSubmit={handleUpdateRoleAssignation}
      />
      <Select
        onChange={setSelectedRole}
        value={selectedRole}
        options={translatedOptions}
        popoverSide="bottom"
        popoverClassName="w-36"
      />
    </div>
  );
};
