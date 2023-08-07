import axios, { AxiosResponse } from "axios";
import { useState } from "react";
import { useTranslation } from 'react-i18next'

import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useToast } from "@/lib/hooks";

import { BrainRoleType } from "../../../../NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";

type UseBrainUserProps = {
  fetchBrainUsers: () => Promise<void>;
  role: BrainRoleType;
  brainId: string;
  email: string;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainUser = ({
  brainId,
  fetchBrainUsers,
  role,
  email,
}: UseBrainUserProps) => {
  const { updateBrainAccess } = useBrainApi();
  const { publish } = useToast();
  const [selectedRole, setSelectedRole] = useState<BrainRoleType>(role);
  const [isRemovingAccess, setIsRemovingAccess] = useState(false);
  const { currentBrain } = useBrainContext();
  const { t } = useTranslation(['translation','brain']);
  const updateSelectedRole = async (newRole: BrainRoleType) => {
    setSelectedRole(newRole);
    try {
      await updateBrainAccess(brainId, email, {
        role: newRole,
      });
      publish({ variant: "success", text: t('userRoleUpdated', { email: email, role: newRole, ns: 'brain' }) });
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
          text: t('userRoleUpdateFailed', { email: email, role: newRole, ns: 'brain' })
        });
      }
    }
  };

  const removeUserAccess = async () => {
    setIsRemovingAccess(true);
    try {
      await updateBrainAccess(brainId, email, {
        role: null,
      });
      publish({ 
        variant: "success", 
        text: t('userRemoved', { email: email, ns: 'brain' })
      });
      void fetchBrainUsers();
    } catch (e) {
      if (axios.isAxiosError(e) && e.response?.data !== undefined) {
        publish({
          variant: "danger",
          text: (
            e.response as AxiosResponse<{
              detail: string;
            }>
          ).data.detail,
        });
      } else {
        publish({
          variant: "danger",
          text: t('userRemoveFailed', { email: email, ns: 'brain' })
        });
      }
    } finally {
      setIsRemovingAccess(false);
    }
  };
  const canRemoveAccess = currentBrain?.role === "Owner";

  return {
    isRemovingAccess,
    removeUserAccess,
    updateSelectedRole,
    selectedRole,
    canRemoveAccess
  };
};
