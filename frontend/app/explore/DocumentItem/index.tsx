"use client";
import Spinner from "@/app/components/ui/Spinner";
import { useSupabase } from "@/app/supabase-provider";
import { useToast } from "@/lib/hooks/useToast";
import axios from "axios";
import {
  Dispatch,
  RefObject,
  SetStateAction,
  Suspense,
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
    if (!session) {
      throw new Error("User session not found");
    }

    const deleteDocument = async (name: string) => {
      setIsDeleting(true);
      try {
        await axios.delete(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/explore/${name}`,
          {
            headers: {
              Authorization: `Bearer ${session.access_token}`,
            },
          }
        );
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
        <p className="text-lg leading-tight max-w-sm">{document.name}</p>
        <div className="flex gap-2 self-end">
          {/* VIEW MODAL */}
          <Modal
            title={document.name}
            desc={""}
            Trigger={<Button className="">View</Button>}
          >
            <Suspense fallback={<Spinner />}>
              {/* @ts-expect-error TODO: check if DocumentData component can be sync */}
              <DocumentData documentName={document.name} />
            </Suspense>
          </Modal>

          {/* DELETE MODAL */}
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
