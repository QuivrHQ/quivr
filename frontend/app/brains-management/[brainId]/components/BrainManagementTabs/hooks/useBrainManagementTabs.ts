import { UUID } from "crypto";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useBrainFetcher } from "./useBrainFetcher";
import { BrainManagementTab } from "../types";
import { getBrainPermissions } from "../utils/getBrainPermissions";
import { getTargetedTab } from "../utils/getTargetedTab";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainManagementTabs = () => {
  const [selectedTab, setSelectedTab] =
    useState<BrainManagementTab>("settings");
  const { allBrains } = useBrainContext();

  useEffect(() => {
    const targetedTab = getTargetedTab();
    if (targetedTab !== undefined) {
      setSelectedTab(targetedTab);
    }
  }, []);

  const { deleteBrain, setCurrentBrainId, fetchAllBrains } = useBrainContext();
  const [
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
  ] = useState(false);
  const router = useRouter();

  const params = useParams();

  const brainId = params?.brainId as UUID | undefined;
  const { hasEditRights, isOwnedByCurrentUser } = getBrainPermissions({
    brainId,
    userAccessibleBrains: allBrains,
  });

  const { brain } = useBrainFetcher({
    brainId,
  });

  const handleUnsubscribeOrDeleteBrain = () => {
    if (brainId === undefined) {
      return;
    }
    try {
      if (!isOwnedByCurrentUser) {
        alert("unscribed");

        return;
      }
      void deleteBrain(brainId);
      setCurrentBrainId(null);
      router.push("/brains-management");
      setIsDeleteOrUnsubscribeModalOpened(false);
      void fetchAllBrains();
    } catch (error) {
      console.error("Error deleting brain: ", error);
    }
  };

  return {
    selectedTab,
    setSelectedTab,
    brainId,
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    brain,
    hasEditRights,
    isOwnedByCurrentUser,
  };
};
