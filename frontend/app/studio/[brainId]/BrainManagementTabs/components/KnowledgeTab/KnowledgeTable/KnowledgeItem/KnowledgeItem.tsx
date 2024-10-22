import axios from "axios";
import { capitalCase } from "change-case";
import Image from "next/image";
import React, { useEffect, useRef, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { KMSElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { OptionsModal } from "@/lib/components/ui/OptionsModal/OptionsModal";
import { Tag } from "@/lib/components/ui/Tag/Tag";
import { iconList } from "@/lib/helpers/iconList";
import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";
import { useDevice } from "@/lib/hooks/useDevice";
import { Option } from "@/lib/types/Options";

import { useKnowledgeItem } from "./hooks/useKnowledgeItem";
// eslint-disable-next-line import/order
import styles from "./KnowledgeItem.module.scss";

const KnowledgeItem = ({
  knowledge,
  selected,
  setSelected,
  lastChild,
}: {
  knowledge: KMSElement;
  selected: boolean;
  setSelected: (selected: boolean, event: React.MouseEvent) => void;
  lastChild?: boolean;
}): JSX.Element => {
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);
  const iconRef = useRef<HTMLDivElement | null>(null);
  const optionsRef = useRef<HTMLDivElement | null>(null);
  const { onDeleteKnowledge } = useKnowledgeItem();
  const { brain } = useUrlBrain();
  const { generateSignedUrlKnowledge } = useKnowledgeApi();
  const { isMobile } = useDevice();
  const { providerIconUrls } = useSync();

  const getOptions = (): Option[] => [
    {
      label: "Delete",
      onClick: () => void onDeleteKnowledge(knowledge),
      iconName: "delete",
      iconColor: "dangerous",
      disabled: brain?.role !== "Owner",
    },
    {
      label: "Download",
      onClick: () => void downloadFile(),
      iconName: "download",
      iconColor: "primary",
      disabled: brain?.role !== "Owner" || !!knowledge.url,
    },
  ];

  const downloadFile = async () => {
    if (!knowledge.url && knowledge.file_name) {
      const downloadUrl = await generateSignedUrlKnowledge({
        knowledgeId: knowledge.id,
      });

      try {
        const response = await axios.get(downloadUrl, {
          responseType: "blob",
        });

        const blobUrl = window.URL.createObjectURL(new Blob([response.data]));

        const a = document.createElement("a");
        a.href = blobUrl;
        a.download = knowledge.file_name;
        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(blobUrl);
      } catch (error) {
        console.error("Error downloading the file:", error);
      }
    }
    setOptionsOpened(false);
  };

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

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const renderIcon = () => {
    if (!knowledge.url) {
      return knowledge.source !== "local" ? (
        <Image
          src={providerIconUrls[knowledge.source]}
          width="16"
          height="16"
          alt="integration_icon"
        />
      ) : (
        <Icon
          name={
            knowledge.extension
              ? (knowledge.extension.slice(1) as keyof typeof iconList)
              : "file"
          }
          size="small"
          color="black"
        />
      );
    }

    return <Icon name="link" size="small" color="black" />;
  };

  const renderFileNameOrUrl = () => {
    if (!knowledge.url) {
      return <span className={styles.file_name}>{knowledge.file_name}</span>;
    }

    return (
      <a href={knowledge.url} target="_blank" rel="noopener noreferrer">
        {knowledge.url}
      </a>
    );
  };

  return (
    <div
      className={`${styles.knowledge_item_wrapper} ${
        lastChild ? styles.last : ""
      }`}
    >
      <div className={styles.left}>
        <Checkbox
          checked={selected}
          setChecked={(checked, event) => setSelected(checked, event)}
        />
        <div className={styles.icon}>{renderIcon()}</div>
        {renderFileNameOrUrl()}
      </div>
      <div className={styles.right}>
        {!isMobile && (
          <div className={styles.status}>
            <Tag
              name={capitalCase(knowledge.status ?? "")}
              color={
                knowledge.status === "ERROR"
                  ? "dangerous"
                  : knowledge.status === "PROCESSING"
                  ? "primary"
                  : "success"
              }
            />
          </div>
        )}
        <div
          ref={iconRef}
          onClick={(event: React.MouseEvent<HTMLElement>) => {
            event.stopPropagation();
            event.preventDefault();
            setOptionsOpened(!optionsOpened);
          }}
        >
          <Icon name="options" size="small" color="black" handleHover={true} />
        </div>
      </div>
      <div ref={optionsRef} className={styles.options_modal}>
        {optionsOpened && <OptionsModal options={getOptions()} />}
      </div>
    </div>
  );
};

export default KnowledgeItem;
