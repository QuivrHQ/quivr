"use client";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";

import { DeleteOrUnsubscribeConfirmationModal } from "@/app/studio/[brainId]/BrainManagementTabs/components/DeleteOrUnsubscribeModal/DeleteOrUnsubscribeConfirmationModal";
import { useBrainManagementTabs } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainManagementTabs";
import { getBrainPermissions } from "@/app/studio/[brainId]/BrainManagementTabs/utils/getBrainPermissions";
import Icon from "@/lib/components/ui/Icon/Icon";
import { OptionsModal } from "@/lib/components/ui/OptionsModal/OptionsModal";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useAddedKnowledge } from "@/lib/hooks/useAddedKnowledge";
import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";
import { Option } from "@/lib/types/Options";

import styles from "./BrainFolder.module.scss";
import KnowledgeItem from "./KnowledgeItem/KnowledgeItem";

type BrainFolderProps = {
  brain: MinimalBrainForUser;
  searchValue: string;
};

const BrainFolder = ({ brain, searchValue }: BrainFolderProps): JSX.Element => {
  const { isDarkMode } = useUserSettingsContext();
  const { allKnowledge } = useAddedKnowledge({
    brainId: brain.id,
  });
  const [folded, setFolded] = useState<boolean>(true);
  const contentRef = useRef<HTMLDivElement>(null);
  const {
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs(brain.id);
  const [storedKnowledge, setStoredKnowledge] = useState<Knowledge[]>([]);
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);

  const { allBrains } = useBrainContext();
  const { isOwnedByCurrentUser } = getBrainPermissions({
    brainId: brain.id,
    userAccessibleBrains: allBrains,
  });

  const iconRef = useRef<HTMLDivElement | null>(null);
  const optionsRef = useRef<HTMLDivElement | null>(null);

  const options: Option[] = [
    {
      label: "Edit",
      onClick: () => (window.location.href = `/studio/${brain.id}`),
      iconName: "edit",
      iconColor: "primary",
    },
    {
      label: "Delete",
      onClick: () => void setIsDeleteOrUnsubscribeModalOpened(true),
      iconName: "delete",
      iconColor: "dangerous",
    },
  ];

  const filteredKnowledge = storedKnowledge
    .filter((knowledge) =>
      isUploadedKnowledge(knowledge)
        ? knowledge.fileName.toLowerCase().includes(searchValue.toLowerCase())
        : knowledge.url.toLowerCase().includes(searchValue.toLowerCase())
    )
    .sort((a, b) => {
      const nameA = isUploadedKnowledge(a) ? a.fileName : a.url;
      const nameB = isUploadedKnowledge(b) ? b.fileName : b.url;

      return nameA.localeCompare(nameB);
    });

  const getContentHeight = (): string => {
    return folded ? "0" : `${contentRef.current?.scrollHeight}px`;
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    const droppedKnowledge = JSON.parse(
      event.dataTransfer.getData("text/plain")
    ) as Knowledge;

    console.log("Dropped knowledge:", droppedKnowledge, "to brain:", brain.id);
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  useEffect(() => {
    setStoredKnowledge([...allKnowledge]);
  }, [allKnowledge, storedKnowledge.length, searchValue]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        iconRef.current &&
        !iconRef.current.contains(event.target as Node) &&
        optionsRef.current &&
        !optionsRef.current.contains(event.target as Node)
      ) {
        setOptionsOpened(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    if (!folded && contentRef.current) {
      contentRef.current.style.maxHeight = `${contentRef.current.scrollHeight}px`;
    } else if (folded && contentRef.current) {
      contentRef.current.style.maxHeight = "0";
    }
  }, [folded, storedKnowledge]);

  return (
    <div
      className={styles.brain_folder_wrapper}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <div
        className={styles.brain_folder_header}
        onClick={() => setFolded(!folded)}
      >
        <div className={styles.left}>
          <Icon
            size="small"
            name="chevronDown"
            color="black"
            classname={`${styles.icon_rotate} ${
              folded ? styles.icon_rotate_down : styles.icon_rotate_right
            }`}
          />
          <Image
            className={isDarkMode ? styles.dark_image : ""}
            src={
              brain.integration_logo_url
                ? brain.integration_logo_url
                : "/default_brain_image.png"
            }
            alt="logo_image"
            width={18}
            height={18}
          />
          <span className={styles.name}>{brain.name}</span>
        </div>
        <div
          className={styles.icon_wrapper}
          ref={iconRef}
          onClick={(event: React.MouseEvent<HTMLElement>) => {
            event.nativeEvent.stopImmediatePropagation();
            event.stopPropagation();
            setOptionsOpened(!optionsOpened);
          }}
        >
          <Icon name="options" size="normal" color="black" handleHover={true} />
        </div>
      </div>
      <div className={styles.options_modal_wrapper}>
        <div ref={optionsRef} className={styles.options_modal}>
          {optionsOpened && <OptionsModal options={options} />}
        </div>
      </div>
      <div
        ref={contentRef}
        className={`${styles.content_wrapper} ${
          folded ? styles.content_collapsed : styles.content_expanded
        }`}
        style={{ maxHeight: getContentHeight() }}
      >
        {filteredKnowledge.map((knowledge) => (
          <div key={knowledge.id} className={styles.knowledge}>
            <KnowledgeItem knowledge={knowledge} />
          </div>
        ))}
      </div>
      <DeleteOrUnsubscribeConfirmationModal
        isOpen={isDeleteOrUnsubscribeModalOpened}
        setOpen={setIsDeleteOrUnsubscribeModalOpened}
        onConfirm={() => void handleUnsubscribeOrDeleteBrain()}
        isOwnedByCurrentUser={isOwnedByCurrentUser}
        isDeleteOrUnsubscribeRequestPending={
          isDeleteOrUnsubscribeRequestPending
        }
      />
    </div>
  );
};

export default BrainFolder;
