import { UUID } from "crypto";

import { KMSElement } from "../api/sync/types";

interface HandleDropParams {
  event: React.DragEvent<HTMLDivElement>;
  targetElement: KMSElement;
  patchKnowledge: (knowledgeId: UUID, parent_id: UUID) => Promise<KMSElement>;
  setRefetchFolderMenu: (value: boolean) => void;
  fetchQuivrFiles: (parentId: UUID | null) => Promise<void>;
  currentFolder: KMSElement | undefined;
}

export const handleDrop = async ({
  event,
  targetElement,
  patchKnowledge,
  setRefetchFolderMenu,
  fetchQuivrFiles,
  currentFolder,
}: HandleDropParams): Promise<void> => {
  event.preventDefault();
  const draggedElement = JSON.parse(
    event.dataTransfer.getData("application/json")
  ) as KMSElement;
  if (draggedElement.id !== targetElement.id) {
    try {
      await patchKnowledge(draggedElement.id, targetElement.id);
      setRefetchFolderMenu(true);
      await fetchQuivrFiles(currentFolder?.id ?? null);
    } catch (error) {
      console.error("Failed to patch knowledge:", error);
    }
  }
};
