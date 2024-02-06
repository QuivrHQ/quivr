import { AnimatePresence, motion } from "framer-motion";

import { KnowledgeToFeed } from "@/app/chat/[chatId]/components/ActionsBar/components";
import { useActionBar } from "@/app/chat/[chatId]/components/ActionsBar/hooks/useActionBar";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

import styles from "./UploadDocumentModal.module.scss";

import { Modal } from "../ui/Modal";

export const UploadDocumentModal = (): JSX.Element => {
  const { shouldDisplayFeedCard, setShouldDisplayFeedCard } =
    useKnowledgeToFeedContext();
  const { setHasPendingRequests } = useActionBar();

  if (!shouldDisplayFeedCard) {
    return <></>;
  }

  return (
    <Modal
      isOpen={shouldDisplayFeedCard}
      setOpen={setShouldDisplayFeedCard}
      CloseTrigger={<div />}
    >
      <div className={styles.knowledge_modal}>
        <AnimatePresence>
          <motion.div
            key="slide"
            initial={{ y: "100%", opacity: 0 }}
            animate={{ y: 0, opacity: 1, transition: { duration: 0.2 } }}
            exit={{ y: "100%", opacity: 0 }}
          >
            <KnowledgeToFeed
              dispatchHasPendingRequests={() => setHasPendingRequests(true)}
            />
          </motion.div>
        </AnimatePresence>
      </div>
    </Modal>
  );
};
