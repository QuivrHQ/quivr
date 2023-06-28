/* eslint-disable max-lines */
import { UUID } from "crypto";
import { useCallback, useEffect, useState } from "react";

import {
  createBrainFromBackend,
  deleteBrainFromBE,
  getAllUserBrainsFromBE,
  getBrainFromBE,
  getUserDefaultBrainFromBackend,
} from "@/lib/api";
import { useAxios, useToast } from "@/lib/hooks";

import {
  getBrainFromLocalStorage,
  saveBrainInLocalStorage,
} from "../helpers/brainLocalStorage";
import { Brain } from "../types";

export interface BrainStateProps {
  currentBrain: Brain | undefined;
  currentBrainId: UUID | null;
  allBrains: Brain[];
  createBrain: (name: string) => Promise<UUID | undefined>;
  deleteBrain: (id: UUID) => Promise<void>;
  setActiveBrain: (id: UUID) => void;
  getBrainWithId: (brainId: UUID) => Promise<Brain>;
  fetchAllBrains: () => Promise<void>;
  setDefaultBrain: () => Promise<void>;
}

export const useBrainState = (): BrainStateProps => {
  const { publish } = useToast();

  const [allBrains, setAllBrains] = useState<Brain[]>([]);
  const [currentBrainId, setCurrentBrainId] = useState<null | UUID>(null);
  const { axiosInstance } = useAxios();

  const currentBrain = allBrains.find((brain) => brain.id === currentBrainId);

  // options: Record<string, string | unknown>;

  const createBrain = async (name: string): Promise<UUID | undefined> => {
    const createdBrain = await createBrainFromBackend(axiosInstance, name);
    if (createdBrain !== undefined) {
      setAllBrains((prevBrains) => [...prevBrains, createdBrain]);
      saveBrainInLocalStorage(createdBrain);

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
    try {
      console.log("Fetching all brains for a user");
      const brains = await getAllUserBrainsFromBE(axiosInstance);
      console.log(brains);
      setAllBrains(brains ?? []);
      console.log("Fetched all brains for user");
    } catch (error) {
      console.error(error);
    }
  }, [axiosInstance]);

  const setActiveBrain = useCallback((id: UUID) => {
    //get brain with id from BE ?

    const newActiveBrain = { id, name: "Default Brain" };
    // if (newActiveBrain) {
    console.log("newActiveBrain", newActiveBrain);
    saveBrainInLocalStorage(newActiveBrain);
    setCurrentBrainId(id);
    console.log("Setting active brain", newActiveBrain);
    // } else {
    //   console.warn(`No brain found with ID ${id}`);
    // }
  }, []);

  const setDefaultBrain = useCallback(async () => {
    console.log("Setting default brain");
    const defaultBrain = await getUserDefaultBrainFromBackend(axiosInstance);
    console.log("defaultBrain", defaultBrain);
    if (defaultBrain) {
      saveBrainInLocalStorage(defaultBrain);
      setActiveBrain(defaultBrain.id);
    } else {
      console.warn("No brains found");
    }
  }, [axiosInstance, setActiveBrain]);

  const fetchAndSetActiveBrain = useCallback(async () => {
    console.log(
      "Fetching and setting active brain use effect in useBrainState"
    );
    const storedBrain = getBrainFromLocalStorage();
    if (storedBrain?.id !== undefined) {
      console.log("Setting active brain from local storage");
      console.log("storedBrain", storedBrain);
      setActiveBrain(storedBrain.id);
    } else {
      console.log("Setting default brain for first time");
      await setDefaultBrain();
    }
  }, [setDefaultBrain, setActiveBrain]);

  useEffect(() => {
    void fetchAllBrains();

    console.log("brainId", currentBrainId);
    void fetchAndSetActiveBrain();
  }, [fetchAllBrains, fetchAndSetActiveBrain, currentBrainId]);

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
  };
};
