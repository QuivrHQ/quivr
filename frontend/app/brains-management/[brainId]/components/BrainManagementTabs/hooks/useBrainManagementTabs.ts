import { UUID } from "crypto";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainManagementTab } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainManagementTabs = () => {
  const [selectedTab, setSelectedTab] =
    useState<BrainManagementTab>("settings");
  const { deleteBrain, setCurrentBrainId } = useBrainContext();
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const router = useRouter();

  const params = useParams();

  const brainId = params?.brainId as UUID | undefined;

  const handleDeleteBrain = () => {
    if (brainId === undefined) {
      return;
    }
    void deleteBrain(brainId);
    setCurrentBrainId(null);
    router.push("/brains-management");
    setIsDeleteModalOpen(false);
  };

  return {
    selectedTab,
    setSelectedTab,
    brainId,
    handleDeleteBrain,
    isDeleteModalOpen,
    setIsDeleteModalOpen,
  };
};
