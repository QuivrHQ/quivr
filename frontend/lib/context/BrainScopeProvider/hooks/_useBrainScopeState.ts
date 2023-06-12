import { Document } from "@/app/explore/types";
import generateUUID from "@/lib/helpers/generateUUID";
import { useAxios } from "@/lib/useAxios";
import { UUID } from "crypto";
import { useEffect, useState } from "react";
import { BrainScope } from "../types";

export default function _useBrainScopeState() {
  const [allBrains, setAllBrains] = useState<BrainScope[]>([]);
  const [currentBrainId, setCurrentBrainId] = useState<null | UUID>(null);
  // currentBrain will change if we change currentBrainIndex or allBrains
  const currentBrain = allBrains.find((brain) => brain.id === currentBrainId);

  const [allDocuments, setAllDocuments] = useState<Document[]>([]);
  const { axiosInstance } = useAxios();

  const createBrain = (name: string, id?: UUID) => {
    let _id = generateUUID();
    setAllBrains((prevBrains) => [
      ...prevBrains,
      { id: id ?? _id, name, documents: [...allDocuments] },
    ]);
  };

  const deleteBrain = (id: UUID) => {
    setAllBrains((prevBrains) => prevBrains.filter((brain) => brain.id !== id));
  };

  const getBrainWithId = (id: UUID) => {
    const brain = allBrains.find((brain) => brain.id === id);
    if (!brain) throw new Error(`Brain with id: ${id} not found`);
    return brain;
  };

  const setActiveBrain = (id: UUID) => {
    setCurrentBrainId(id);
  };

  const removeDocumentFromBrain = (brainId: UUID, sha1: string) => {
    const brains = [...allBrains];
    brains.forEach((brain) => {
      if (brain.id === brainId) {
        brain.documents = brain.documents.filter((doc) => doc.sha1 !== sha1);
        return; // return as there cannot be more than one brain with that id
      }
    });
    setAllBrains(brains);
  };
  const addDocumentToBrain = (brainId: UUID, document: Document) => {
    const brains = [...allBrains];
    brains.forEach((brain) => {
      if (brain.id === brainId) {
        brain.documents.push(document);
        return; // return as there cannot be more than one brain with that id
      }
    });
    setAllBrains(brains);
  };

  useEffect(() => {
    (async () => {
      const response = await axiosInstance.get<{ documents: Document[] }>(
        "/explore"
      );
      setAllDocuments(response.data.documents);
      // TODO: redo logic to fetch brains from db or localstorage
      setAllBrains([
        {
          name: "Super Brain",
          id: "super-duper-brain",
          documents: response.data.documents,
        },
      ]);
    })();
  }, []);

  return {
    currentBrain,
    allBrains,
    createBrain,
    deleteBrain,
    setActiveBrain,
    addDocumentToBrain,
    removeDocumentFromBrain,
  };
}
