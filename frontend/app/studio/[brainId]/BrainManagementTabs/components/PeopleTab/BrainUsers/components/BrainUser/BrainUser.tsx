import { Select } from "@/lib/components/ui/Select";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { RemoveAccessIcon } from "./components/RemoveAccessIcon";
import { useBrainUser } from "./hooks/useBrainUser";

import { availableRoles, BrainRoleType } from "../../types";

type BrainUserProps = {
  email: string;
  role: BrainRoleType;
  brainId: string;
  fetchBrainUsers: () => Promise<void>;
};

export const BrainUser = ({
  email,
  role,
  brainId,
  fetchBrainUsers,
}: BrainUserProps): JSX.Element => {
  const {
    isRemovingAccess,
    canRemoveAccess,
    selectedRole,
    removeUserAccess,
    updateSelectedRole,
  } = useBrainUser({
    fetchBrainUsers: fetchBrainUsers,
    role,
    brainId,
    email,
  });
  const { currentBrain } = useBrainContext();

  return (
    <div
      data-testid="assignation-row"
      className="flex flex-row align-center my-2 gap-3 items-center"
    >
      {canRemoveAccess && (
        <RemoveAccessIcon
          isRemovingAccess={isRemovingAccess}
          onClick={() => void removeUserAccess()}
        />
      )}
      <div className="flex flex-1">
        <TextInput label="Email" inputValue={email} disabled={true} />
      </div>
      <Select
        onChange={(newRole) => void updateSelectedRole(newRole)}
        value={selectedRole}
        options={availableRoles}
        readOnly={currentBrain?.role !== "Owner" && selectedRole === "Owner"}
      />
    </div>
  );
};
