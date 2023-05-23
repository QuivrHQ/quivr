"use client";
import { Document } from "./types";
import Button from "../components/ui/Button";
import Modal from "../components/ui/Modal";
import { AnimatedCard } from "../components/ui/Card";
import { useState } from "react";
import axios from "axios";

interface DocumentProps {
  document: Document;
}

const DocumentItem = ({ document }: DocumentProps) => {
  const [isDeleting, setIsDeleting] = useState(false);

  const deleteDocument = async (name: string) => {
    setIsDeleting(true);
    try {
      console.log(`Deleting Document ${name}`);
      const response = await axios.delete(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/explore/${name}`
      );
    } catch (error) {
      console.error(`Error deleting ${name}`, error);
    }
    setIsDeleting(false);
  };

  return (
    <AnimatedCard
      initial={{ x: -64, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="flex items-center justify-between w-full p-5 gap-10"
    >
      <p className="text-lg leading-tight max-w-sm">{document.name}</p>
      <div className="flex gap-2">
        <Modal
          title={document.name}
          desc={""}
          Trigger={<Button className="">View</Button>}
        >
          <div className="bg-white py-10 w-full h-1/2 overflow-auto rounded-lg prose">
            <pre>{JSON.stringify(document, null, 2)}</pre>
          </div>
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
};

DocumentItem.displayName = "DocumentItem";
export default DocumentItem;
