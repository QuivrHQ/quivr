/* eslint-disable */
"use client";
import {
  Dispatch,
  forwardRef,
  RefObject,
  SetStateAction,
  useState,
} from "react";

import Button from "@/lib/components/ui/Button";
import { AnimatedCard } from "@/lib/components/ui/Card";
import Ellipsis from "@/lib/components/ui/Ellipsis";
import { Modal } from "@/lib/components/ui/Modal";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useAxios, useToast } from "@/lib/hooks";
import { Document } from "@/lib/types/Document";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import DocumentData from "./DocumentData";
import { useTranslation } from "react-i18next";

interface DocumentProps {
  document: Document;
  setDocuments: Dispatch<SetStateAction<Document[]>>;
}

const DocumentItem = forwardRef(
  ({ document, setDocuments }: DocumentProps, forwardedRef) => {
    const [isDeleting, setIsDeleting] = useState(false);
    const { publish } = useToast();
    const { session } = useSupabase();
    const { axiosInstance } = useAxios();
    const { track } = useEventTracking();
    const { currentBrain } = useBrainContext();

    const canDeleteFile = currentBrain?.role === "Owner";
    const {t} = useTranslation(["translation","explore"]);

    if (!session) {
      throw new Error(t("sessionNotFound", {ns: "explore"}));
    }

    const deleteDocument = async (name: string) => {
      setIsDeleting(true);
      void track("DELETE_DOCUMENT");
      try {
        if (currentBrain?.id === undefined)
          throw new Error(t("noBrain", {ns: "explore"}));
        await axiosInstance.delete(
          `/explore/${name}/?brain_id=${currentBrain.id}`
        );
        setDocuments((docs) => docs.filter((doc) => doc.name !== name)); // Optimistic update
        publish({
          variant: "success",
          text: t("deleted", {fileName: name, brain: currentBrain.name, ns: "explore"})
        });
      } catch (error) {
        publish({
          variant: "warning",
          text: t("errorDeleting", {fileName: name, ns: "explore"})
        });
        console.error(`Error deleting ${name}`, error);
      }
      setIsDeleting(false);
    };

    return (
      <AnimatedCard
        initial={{ x: -64, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        exit={{ x: 64, opacity: 0 }}
        layout
        ref={forwardedRef as RefObject<HTMLDivElement>}
        className="flex flex-col sm:flex-row sm:items-center justify-between w-full p-5 gap-5"
      >
        <Ellipsis tooltip maxCharacters={30}>
          {document.name}
        </Ellipsis>
        <div className="flex gap-2 self-end">
          <Modal Trigger={<Button className="">{t("view", {ns: "explore"})}</Button>}>
            <DocumentData documentName={document.name} />
          </Modal>

          {canDeleteFile && (
            <Modal
            title={t("deleteConfirmTitle",{ns: "explore"})}
            desc={t("deleteConfirmText",{ns: "explore"})}
            Trigger={
              <Button isLoading={isDeleting} variant={"danger"} className="">
                {t("deleteButton")}
              </Button>
            }
            CloseTrigger={
              <Button
                variant={"danger"}
                isLoading={isDeleting}
                onClick={() => {
                  deleteDocument(document.name);
                }}
                className="self-end"
              >
                {t("deleteForeverButton")}
              </Button>
            }
          >
            <p>{document.name}</p>
          </Modal>
          )}
        </div>
      </AnimatedCard>
    );
  }
);

DocumentItem.displayName = "DocumentItem";
export default DocumentItem;
