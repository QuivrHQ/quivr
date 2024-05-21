"use client";

import axios from "axios";
import { useEffect, useRef, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import Icon from "@/lib/components/ui/Icon/Icon";
import { OptionsModal } from "@/lib/components/ui/OptionsModal/OptionsModal";
import { useNotesEditorContext } from "@/lib/context/NotesEditorProvider/hooks/useNotesEditorContext";
import { isUploadedKnowledge, Knowledge } from "@/lib/types/Knowledge";
import { Option } from "@/lib/types/Options";

import styles from "./KnowledgeItem.module.scss";

type KnowledgeItemProps = {
  knowledge: Knowledge;
};

const KnowledgeItem = ({ knowledge }: KnowledgeItemProps): JSX.Element => {
  const { generateSignedUrlKnowledge } = useKnowledgeApi();
  const { updateContent } = useNotesEditorContext();
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);
  const [dragActivated, setDragActivated] = useState<boolean>(false);

  const iconRef = useRef<HTMLDivElement | null>(null);
  const optionsRef = useRef<HTMLDivElement | null>(null);

  const canReadFile = (fileName: string): boolean => {
    const extension = fileName.split(".").pop();

    return (
      (extension === "txt" || extension === "md") &&
      isUploadedKnowledge(knowledge)
    );
  };

  const options: Option[] = [
    {
      label: "Edit",
      onClick: () => void logFileContent(),
      iconName: "edit",
      iconColor: "primary",
      disabled: isUploadedKnowledge(knowledge)
        ? !canReadFile(knowledge.fileName)
        : false,
    },
    {
      label: "Delete",
      onClick: () => void true,
      iconName: "delete",
      iconColor: "dangerous",
    },
  ];

  const handleDragStart = (event: React.DragEvent<HTMLDivElement>) => {
    event.dataTransfer.setData("text/plain", JSON.stringify(knowledge));
  };

  const logFileContent = async () => {
    if (isUploadedKnowledge(knowledge)) {
      let download_url = await generateSignedUrlKnowledge({
        knowledgeId: knowledge.id,
      });
      download_url = download_url.replace("host.docker.internal", "localhost");

      try {
        const response = await axios.get(download_url, {
          responseType: "blob",
        });

        const reader = new FileReader();

        reader.onload = (event) => {
          const text = event.target?.result as string;
          const html = text.replace(/\n/g, "<br/>");
          updateContent(html);
        };

        reader.onerror = (event) => {
          console.error("Error reading file:", event);
        };

        reader.readAsText(new Blob([response.data]));
      } catch (error) {
        console.error("Error downloading the file:", error);
      }
    }
  };

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

  return (
    <div
      className={`${styles.knowledge_item_container} ${
        dragActivated ? styles.dragging : ""
      }`}
      draggable
      onDragStart={(event) => {
        handleDragStart(event);
        setDragActivated(true);
      }}
      onDragEnd={() => setDragActivated(false)}
    >
      <div
        className={`${styles.knowledge_item_wrapper} ${
          !canReadFile(
            isUploadedKnowledge(knowledge) ? knowledge.fileName : knowledge.url
          )
            ? styles.disabled
            : ""
        }`}
      >
        {isUploadedKnowledge(knowledge) ? (
          <span className={styles.name}>{knowledge.fileName}</span>
        ) : (
          <a
            className={styles.name}
            href={knowledge.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            {knowledge.url}
          </a>
        )}
        <div
          className={styles.icon_wrapper}
          ref={iconRef}
          onClick={(event: React.MouseEvent<HTMLElement>) => {
            event.nativeEvent.stopImmediatePropagation();
            event.stopPropagation();
            setOptionsOpened(!optionsOpened);
          }}
        >
          <Icon name="options" size="tiny" color="black" handleHover={true} />
        </div>
      </div>
      <div className={styles.options_modal_wrapper}>
        <div ref={optionsRef} className={styles.options_modal}>
          {optionsOpened && <OptionsModal options={options} />}
        </div>
      </div>
    </div>
  );
};

export default KnowledgeItem;
