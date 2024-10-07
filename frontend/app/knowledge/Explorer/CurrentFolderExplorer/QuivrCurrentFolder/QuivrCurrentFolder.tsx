import { UUID } from "crypto";
import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { KMSElement } from "@/lib/api/sync/types";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import AddFolderModal from "./AddFolderModal/AddFolderModal";
import styles from "./QuivrCurrentFolder.module.scss";

import { useKnowledgeContext } from "../../../KnowledgeProvider/hooks/useKnowledgeContext";
import CurrentFolderExplorerLine from "../../shared/CurrentFolderExplorerLine/CurrentFolderExplorerLine";
import FolderExplorerHeader from "../../shared/FolderExplorerHeader/FolderExplorerHeader";

const QuivrCurrentFolder = (): JSX.Element => {
  const [loading, setLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [addFolderModalOpened, setAddFolderModalOpened] = useState(false);
  const [quivrElements, setQuivrElements] = useState<KMSElement[]>();
  const {
    currentFolder,
    exploringQuivr,
    selectedKnowledges,
    setSelectedKnowledges,
    setRefetchFolderMenu,
  } = useKnowledgeContext();
  const { getFiles, deleteKnowledge, patchKnowledge } = useKnowledgeApi();

  const fetchQuivrFiles = async (folderId: UUID | null) => {
    setLoading(true);
    try {
      const res = await getFiles(folderId);
      setQuivrElements(res);
    } catch (error) {
      console.error("Failed to get sync files:", error);
    } finally {
      setLoading(false);
      console.info("hey");
    }
  };

  const deleteKnowledges = async () => {
    setDeleteLoading(true);
    try {
      await Promise.all(
        selectedKnowledges.map((knowledge) =>
          deleteKnowledge({ knowledgeId: knowledge.id })
        )
      );
      await fetchQuivrFiles(currentFolder?.id ?? null);
      setSelectedKnowledges([]);
    } catch (error) {
      console.error("Failed to delete knowledges:", error);
    } finally {
      setDeleteLoading(false);
      setRefetchFolderMenu(true);
    }
  };

  useEffect(() => {
    if (exploringQuivr) {
      void fetchQuivrFiles(currentFolder?.id ?? null);
    }
  }, [currentFolder]);

  useEffect(() => {
    if (!addFolderModalOpened) {
      void fetchQuivrFiles(currentFolder?.id ?? null);
    }
  }, [addFolderModalOpened]);

  const handleDragStart = (
    event: React.DragEvent<HTMLDivElement>,
    element: KMSElement
  ) => {
    event.dataTransfer.setData("application/json", JSON.stringify(element));
  };

  const handleDrop = async (
    event: React.DragEvent<HTMLDivElement>,
    targetElement: KMSElement
  ) => {
    event.preventDefault();
    const draggedElement = JSON.parse(
      event.dataTransfer.getData("application/json")
    ) as KMSElement;
    try {
      await patchKnowledge(draggedElement.id, targetElement.id);
      setRefetchFolderMenu(true);
      await fetchQuivrFiles(currentFolder?.id ?? null);
    } catch (error) {
      console.error("Failed to patch knowledge:", error);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  return (
    <>
      <div className={styles.main_container}>
        <FolderExplorerHeader />
        <div className={styles.current_folder_content}>
          {loading ? (
            <div className={styles.loading_icon}>
              <LoaderIcon size="large" color="primary" />
            </div>
          ) : (
            <>
              <div className={styles.content_header}>
                <QuivrButton
                  iconName="delete"
                  label="Delete"
                  color="dangerous"
                  onClick={() => void deleteKnowledges()}
                  small={true}
                  isLoading={deleteLoading}
                  disabled={!selectedKnowledges.length}
                />
                <QuivrButton
                  iconName="add"
                  label="Add Folder"
                  color="primary"
                  onClick={() => setAddFolderModalOpened(true)}
                  small={true}
                />
              </div>
              {quivrElements
                ?.sort((a, b) => Number(b.is_folder) - Number(a.is_folder))
                .map((element, index) => (
                  <div key={index}>
                    <CurrentFolderExplorerLine
                      element={{
                        ...element,
                        parentKMSElement: currentFolder,
                      }}
                      onDragStart={handleDragStart}
                      onDrop={
                        element.is_folder
                          ? (event) => void handleDrop(event, element)
                          : undefined
                      }
                      onDragOver={
                        element.is_folder ? handleDragOver : undefined
                      }
                    />
                  </div>
                ))}
            </>
          )}
        </div>
      </div>
      <AddFolderModal
        isOpen={addFolderModalOpened}
        setIsOpen={setAddFolderModalOpened}
      />
    </>
  );
};

export default QuivrCurrentFolder;
