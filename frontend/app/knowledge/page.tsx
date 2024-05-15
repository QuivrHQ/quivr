"use client";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { ButtonType } from "@/lib/types/QuivrButton";

import KnowledgeList from "./KnowledgeList/KnowledgeList";
import NotesEditor from "./NotesEditor/NotesEditor";
import styles from "./page.module.scss";

const Knowledge = (): JSX.Element => {
  const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();

  const buttons: ButtonType[] = [
    {
      label: "Add knowledge",
      color: "primary",
      onClick: () => {
        setShouldDisplayFeedCard(true);
      },
      iconName: "uploadFile",
    },
    {
      label: "New Note",
      color: "primary",
      onClick: () => {
        console.info("New");
      },
      iconName: "add",
    },
  ];

  return (
    <div className={styles.page_wrapper}>
      <div className={styles.page_header}>
        <PageHeader iconName="book" label="Knowledge" buttons={buttons} />
      </div>
      <div className={styles.content_wrapper}>
        <KnowledgeList />
        <NotesEditor />
      </div>
      <UploadDocumentModal />
    </div>
  );
};

export default Knowledge;
