/* eslint-disable max-lines */
import { UUID } from "crypto";
import { useCallback, useState } from "react";

import {
  createBrainFromBackend,
  deleteBrainFromBE,
  getAllUserBrainsFromBE,
  getBrainFromBE,
  getUserDefaultBrainFromBackend,
} from "@/lib/api";
import { useAxios, useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import {
  getBrainFromLocalStorage,
  saveBrainInLocalStorage,
} from "../helpers/brainLocalStorage";
import { Brain } from "../types";

// CAUTION: This hook should be use in BrainProvider only. You may be need `useBrainContext` instead.

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainProvider = () => {
  const { publish } = useToast();
  const { track } = useEventTracking();
  const { axiosInstance } = useAxios();

  const [allBrains, setAllBrains] = useState<Brain[]>([]);
  const [currentBrainId, setCurrentBrainId] = useState<null | UUID>(null);
  const [isFetchingBrains, setIsFetchingBrains] = useState(false);

  const currentBrain = allBrains.find((brain) => brain.id === currentBrainId);

  const createBrain = async (name: string): Promise<UUID | undefined> => {
    const createdBrain = await createBrainFromBackend(axiosInstance, name);
    if (createdBrain !== undefined) {
      setAllBrains((prevBrains) => [...prevBrains, createdBrain]);
      saveBrainInLocalStorage(createdBrain);
      void track("BRAIN_CREATED");

      return createdBrain.id;
    } else {
      publish({
        variant: "danger",
        text: "Error occured while creating a brain",
      });
    }
  };

  const deleteBrain = async (id: UUID) => {
    await deleteBrainFromBE(axiosInstance, id);
    setAllBrains((prevBrains) => prevBrains.filter((brain) => brain.id !== id));
    void track("DELETE_BRAIN");
  };

  const getBrainWithId = async (brainId: UUID): Promise<Brain> => {
    const brain =
      allBrains.find(({ id }) => id === brainId) ??
      (await getBrainFromBE(axiosInstance, brainId));

    if (brain === undefined) {
      throw new Error(`Error finding brain ${brainId}`);
    }

    return brain;
  };

  const fetchAllBrains = useCallback(async () => {
    setIsFetchingBrains(true);
    try {
      const brains = await getAllUserBrainsFromBE(axiosInstance);
      setAllBrains(brains ?? []);
    } catch (error) {
      console.error(error);
    } finally {
      setIsFetchingBrains(false);
    }
  }, [axiosInstance]);

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
    const defaultBrain = await getUserDefaultBrainFromBackend(axiosInstance);
    if (defaultBrain !== undefined) {
      saveBrainInLocalStorage(defaultBrain);
      setActiveBrain({ ...defaultBrain });
    } else {
      console.warn("No brains found");
    }
  }, [axiosInstance, setActiveBrain]);

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
    createBrain,
    deleteBrain,
    setActiveBrain,
    getBrainWithId,
    fetchAllBrains,
    setDefaultBrain,
    fetchAndSetActiveBrain,
    isFetchingBrains,
    setIsFetchingBrains,
  };
};
