/* eslint-disable max-lines */
import { AxiosInstance } from "axios";
import { UUID } from "crypto";
import { useCallback, useEffect, useState } from "react";

import { useAxios, useToast } from "@/lib/hooks";

import { Brain } from "../types";


const createBrainFromBackend = async (
  axiosInstance: AxiosInstance,
  name: string
): Promise<Brain | undefined> => {
  try {
    const createdBrain = (await axiosInstance.post<Brain>(`/brains`, { name }))
      .data;

    return createdBrain;
  } catch (error) {
    console.error(`Error creating brain ${name}`, error);
  }
};

const getBrainFromBE = async (
  axiosInstance: AxiosInstance,
  brainId: UUID
): Promise<Brain | undefined> => {
  try {
    const brain = (await axiosInstance.get<Brain>(`/brains/${brainId}`)).data;

    return brain;
  } catch (error) {
    console.error(`Error getting brain ${brainId}`, error);

    throw new Error(`Error getting brain ${brainId}`);
  }
};

const deleteBrainFromBE = async (
  axiosInstance: AxiosInstance,
  brainId: UUID
): Promise<void> => {
  try {
    (await axiosInstance.delete(`/brain/${brainId}`)).data;
  } catch (error) {
    console.error(`Error deleting brain ${brainId}`, error);

    throw new Error(`Error deleting brain ${brainId}`);
  }
};

const getAllUserBrainsFromBE = async (
  axiosInstance: AxiosInstance
): Promise<Brain[] | undefined> => {
  try {
    const brains = (await axiosInstance.get<{ brains: Brain[] }>(`/brains`))
      .data;

    console.log("BRAINS", brains);

    return brains.brains;
  } catch (error) {
    console.error(`Error getting brain  for current user}`, error);

    throw new Error(`Error getting brain  for current user`);
  }
};

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
