/* eslint-disable max-lines */
import axios from "axios";
import { useState } from "react";
import { MdOutlineRemoveCircle, MdOutlineTimelapse } from "react-icons/md";

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import Field from "@/lib/components/ui/Field";
import { Select } from "@/lib/components/ui/Select";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useToast } from "@/lib/hooks";

import { BrainRoleType } from "../../../../types";
import { availableRoles } from "../../types";

type BrainUserProps = {
  email: string;
  rights: BrainRoleType;
  brainId: string;
  fetchBrainUsers: () => Promise<void>;
};

export const BrainUser = ({
  email,
  rights,
  brainId,
  fetchBrainUsers,
}: BrainUserProps): JSX.Element => {
  const { updateBrainAccess } = useBrainApi();
  const { publish } = useToast();
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>(rights);
  const [isRemovingAccess, setIsRemovingAccess] = useState(false);
  const { currentBrain } = useBrainContext();
  const updateSelectedRole = async (newRole: BrainRoleType) => {
    setSelectedRole(newRole);
    try {
      await updateBrainAccess(brainId, email, {
        rights: newRole,
      });
      publish({ variant: "success", text: `Updated ${email} to ${newRole}` });
      void fetchBrainUsers();
    } catch (e) {
      if (axios.isAxiosError(e) && e.response?.status === 403) {
        publish({
          variant: "danger",
          text: `${JSON.stringify(
            (
              e.response as {
                data: { detail: string };
              }
            ).data.detail
          )}`,
        });
      } else {
        publish({
          variant: "danger",
          text: `Failed to update ${email} to ${newRole}`,
        });
      }
    }
  };

  const removeUserAccess = async () => {
    setIsRemovingAccess(true);
    try {
      await updateBrainAccess(brainId, email, {
        rights: null,
      });
      publish({ variant: "success", text: `Removed ${email} from brain` });
      void fetchBrainUsers();
    } catch (e) {
      publish({
        variant: "danger",
        text: `Failed to remove ${email} from brain`,
      });
    } finally {
      setIsRemovingAccess(false);
    }
  };

  return (
    <div
      data-testid="assignation-row"
      className="flex flex-row align-center my-2 gap-3 items-center"
    >
      {isRemovingAccess ? (
        <div className="animate-pulse">
          <MdOutlineTimelapse />
        </div>
      ) : (
        <div className="cursor-pointer" onClick={() => void removeUserAccess()}>
          <MdOutlineRemoveCircle />
        </div>
      )}
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
        onChange={(newRole) => void updateSelectedRole(newRole)}
        value={selectedRole}
        options={availableRoles}
        readOnly={currentBrain?.rights !== "Owner" && selectedRole === "Owner"}
      />
    </div>
  );
};
