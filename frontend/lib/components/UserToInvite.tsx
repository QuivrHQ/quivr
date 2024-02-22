import { useState } from "react";
import { useTranslation } from "react-i18next";

import { Select } from "@/lib/components/ui/Select";

import { BrainRoleType } from "./BrainUsers/types";
import { userRoleToAssignableRoles } from "./ShareBrain/types";
import { TextInput } from "./ui/TextInput/TextInput";

export const UserToInvite = (): JSX.Element => {
  const { t } = useTranslation("translation");
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>("Viewer");
  const [email, setEmail] = useState("");

  const assignableRoles = userRoleToAssignableRoles["Owner"];
  const translatedOptions = assignableRoles.map((role) => ({
    value: role.value,
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    label: t(role.value),
  }));

  return (
    <div className="flex flex-row align-center my-2 gap-3 items-center">
      <TextInput label="Email" inputValue={email} setInputValue={setEmail} />
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
