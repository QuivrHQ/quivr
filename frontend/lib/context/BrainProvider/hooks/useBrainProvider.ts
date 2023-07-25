/* eslint-disable max-lines */
import { UUID } from "crypto";
import { useCallback, useState } from "react";

import { CreateBrainInput } from "@/lib/api/brain/brain";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import {
  getBrainFromLocalStorage,
  saveBrainInLocalStorage,
} from "../helpers/brainLocalStorage";
import { MinimalBrainForUser } from "../types";

// CAUTION: This hook should be use in BrainProvider only. You may be need `useBrainContext` instead.

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainProvider = () => {
  const { publish } = useToast();
  const { track } = useEventTracking();
  const { createBrain, deleteBrain, getBrains, getDefaultBrain } =
    useBrainApi();

  const [allBrains, setAllBrains] = useState<MinimalBrainForUser[]>([]);
  const [currentBrainId, setCurrentBrainId] = useState<null | UUID>(null);
  const [isFetchingBrains, setIsFetchingBrains] = useState(false);

  const currentBrain = allBrains.find((brain) => brain.id === currentBrainId);

  const createBrainHandler = async (
    brain: CreateBrainInput
  ): Promise<UUID | undefined> => {
    const createdBrain = await createBrain(brain);
    try {
      setAllBrains((prevBrains) => [...prevBrains, createdBrain]);
      saveBrainInLocalStorage(createdBrain);
      void track("BRAIN_CREATED");

      return createdBrain.id;
    } catch {
      publish({
        variant: "danger",
        text: "Error occurred while creating a brain",
      });
    }
  };

  const deleteBrainHandler = async (id: UUID) => {
    await deleteBrain(id);
    setAllBrains((prevBrains) => prevBrains.filter((brain) => brain.id !== id));
    void track("DELETE_BRAIN");
    publish({
      variant: "success",
      text: "Brain deleted",
    });
  };

  const fetchAllBrains = useCallback(async () => {
    setIsFetchingBrains(true);
    try {
      const brains = await getBrains();
      setAllBrains(brains);
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingBrains(false);
    }
  }, []);

  const setActiveBrain = useCallback(
    ({ id, name }: { id: UUID; name: string }) => {
      const newActiveBrain = { id, name };
      saveBrainInLocalStorage(newActiveBrain);
      setCurrentBrainId(id);
      void track("CHANGE_BRAIN");
    },
    []
  );

  const setDefaultBrain = useCallback(async () => {
    const defaultBrain = await getDefaultBrain();
    if (defaultBrain !== undefined) {
      saveBrainInLocalStorage(defaultBrain);
      setActiveBrain({ ...defaultBrain });
    } else {
      console.warn("No brains found");
    }
  }, [setActiveBrain]);

  const fetchAndSetActiveBrain = useCallback(async () => {
    const storedBrain = getBrainFromLocalStorage();
    if (storedBrain?.id !== undefined) {
      setActiveBrain({ ...storedBrain });
    } else {
      await setDefaultBrain();
    }
  }, [setDefaultBrain, setActiveBrain]);

  return {
    currentBrain,
    currentBrainId,
    allBrains,
    createBrain: createBrainHandler,
    deleteBrain: deleteBrainHandler,
    setActiveBrain,
    fetchAllBrains,
    setDefaultBrain,
    fetchAndSetActiveBrain,
    isFetchingBrains,
  };
};
