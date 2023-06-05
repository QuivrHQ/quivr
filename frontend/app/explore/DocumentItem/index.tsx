"use client";
import Ellipsis from "@/app/components/ui/Ellipsis";
import { useSupabase } from "@/app/supabase-provider";
import { useToast } from "@/lib/hooks/useToast";
import { useAxios } from "@/lib/useAxios";
import {
  Dispatch,
  RefObject,
  SetStateAction,
  forwardRef,
  useState,
} from "react";
import Button from "../../components/ui/Button";
import { AnimatedCard } from "../../components/ui/Card";
import Modal from "../../components/ui/Modal";
import { Document } from "../types";
import DocumentData from "./DocumentData";

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

    if (!session) {
      throw new Error("User session not found");
    }

    const deleteDocument = async (name: string) => {
      setIsDeleting(true);
      try {
        await axiosInstance.delete(`/explore/${name}`);
        setDocuments((docs) => docs.filter((doc) => doc.name !== name)); // Optimistic update
        publish({ variant: "success", text: `${name} deleted.` });
      } catch (error) {
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
          <Modal Trigger={<Button className="">View</Button>}>
            <DocumentData documentName={document.name} />
          </Modal>

          <Modal
            title={"Confirm"}
            desc={`Do you really want to delete?`}
            Trigger={
              <Button isLoading={isDeleting} variant={"danger"} className="">
                Delete
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
                Delete forever
              </Button>
            }
          >
            <p>{document.name}</p>
          </Modal>
        </div>
      </AnimatedCard>
    );
  }
);

DocumentItem.displayName = "DocumentItem";
export default DocumentItem;
