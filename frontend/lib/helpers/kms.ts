import { UUID } from "crypto";

import { KMSElement } from "../api/sync/types";

interface HandleDropParams {
  event: React.DragEvent<HTMLDivElement>;
  targetElement: KMSElement | null;
  patchKnowledge: (
    knowledgeId: UUID,
    parent_id: UUID | null
  ) => Promise<KMSElement>;
  setRefetchFolderMenu: (value: boolean) => void;
  fetchQuivrFiles?: (parentId: UUID | null) => Promise<void>;
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
  if (draggedElement.id !== targetElement?.id) {
    try {
      await patchKnowledge(draggedElement.id, targetElement?.id ?? null);
      setRefetchFolderMenu(true);
      if (fetchQuivrFiles) {
        await fetchQuivrFiles(currentFolder?.id ?? null);
      } else {
        const customEvent = new CustomEvent("needToFetch", {
          detail: { draggedElement, targetElement },
        });
        window.dispatchEvent(customEvent);
      }
    } catch (error) {
      console.error("Failed to patch knowledge:", error);
    }
  }
};

export const handleDragOver = (
  event: React.DragEvent<HTMLDivElement>
): void => {
  event.preventDefault();
};
