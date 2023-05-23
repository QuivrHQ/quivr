"use client";
import { Document } from "../types";
import Button from "../../components/ui/Button";
import Modal from "../../components/ui/Modal";
import { AnimatedCard } from "../../components/ui/Card";
import { Dispatch, SetStateAction, Suspense, useState } from "react";
import axios from "axios";
import DocumentData from "./DocumentData";
import Spinner from "@/app/components/ui/Spinner";

interface DocumentProps {
  document: Document;
  setDocuments: Dispatch<SetStateAction<Document[]>>;
}

const DocumentItem = ({ document, setDocuments }: DocumentProps) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const deleteDocument = async (name: string) => {
    setIsDeleting(true);
    try {
      console.log(`Deleting Document ${name}`);
      const response = await axios.delete(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/explore/${name}`
      );
      setDocuments((docs) => docs.filter((doc) => doc.name !== name)); // Optimistic update
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
      className="flex items-center justify-between w-full p-5 gap-10"
    >
      <p className="text-lg leading-tight max-w-sm">{document.name}</p>
      <div className="flex gap-2">
        {/* VIEW MODAL */}
        <Modal
          title={document.name}
          desc={""}
          Trigger={<Button className="">View</Button>}
        >
          <Suspense fallback={<Spinner />}>
            {/* @ts-expect-error */}
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
};

DocumentItem.displayName = "DocumentItem";
export default DocumentItem;
