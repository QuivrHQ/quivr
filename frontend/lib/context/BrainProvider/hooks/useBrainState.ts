/* eslint-disable max-lines */
import { UUID } from "crypto";
import { useCallback, useEffect, useState } from "react";

import {
  createBrainFromBackend,
  deleteBrainFromBE,
  getAllUserBrainsFromBE,
  getBrainFromBE,
} from "@/lib/api";
import { useAxios, useToast } from "@/lib/hooks";

import { Brain } from "../types";

export interface BrainStateProps {
  currentBrain: Brain | undefined;
  allBrains: Brain[];
  createBrain: (name: string) => Promise<void>;
  deleteBrain: (id: UUID) => Promise<void>;
  setActiveBrain: (id: UUID) => void;
  getBrainWithId: (brainId: UUID) => Promise<Brain>;
  fetchAllBrains: () => Promise<void>;
}

export const useBrainState = (): BrainStateProps => {
  const { publish } = useToast();

  const [allBrains, setAllBrains] = useState<Brain[]>([]);
  const [currentBrainId, setCurrentBrainId] = useState<null | UUID>(null);
  const { axiosInstance } = useAxios();

  const currentBrain = allBrains.find((brain) => brain.id === currentBrainId);

  const setActiveBrain = (id: UUID) => {
    setCurrentBrainId(id);
  };
  // options: Record<string, string | unknown>;

  const createBrain = async (name: string) => {
    const createdBrain = await createBrainFromBackend(axiosInstance, name);
    if (createdBrain !== undefined) {
      setAllBrains((prevBrains) => [...prevBrains, createdBrain]);
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

  // const addDocumentToBrain = (brainId: UUID, document: Document) => {
  //   const brains = [...allBrains];
  //   brains.forEach((brain) => {
  //     if (brain.id === brainId) {
  //       brain.documents?.push(document);

  //       return; // return as there cannot be more than one brain with that id
  //     }
  //   });
  //   //call update brain with document -> need file sha1
  //   setAllBrains(brains);
  // };
  // const removeDocumentFromBrain = (brainId: UUID, sha1: string) => {
  //   const brains = [...allBrains];
  //   brains.forEach((brain) => {
  //     if (brain.id === brainId) {
  //       brain.documents = brain.documents?.filter((doc) => doc.sha1 !== sha1);

  //       //remove document endpoint here (use the document hook ?)

  //       return; // return as there cannot be more than one brain with that id
  //     }
  //   });
  //   setAllBrains(brains);
  // };

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

  useEffect(() => {
    void fetchAllBrains();
  }, [fetchAllBrains]);

  return {
    currentBrain,
    allBrains,
    createBrain,
    deleteBrain,
    setActiveBrain,
    // addDocumentToBrain,
    // removeDocumentFromBrain,
    getBrainWithId,
    fetchAllBrains,
  };
};
