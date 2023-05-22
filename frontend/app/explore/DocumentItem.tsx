"use client";
import { FC } from "react";
import { Document } from "./types";
import Button from "../components/ui/Button";
import Modal from "../components/ui/Modal";
import { AnimatedCard } from "../components/ui/Card";

interface DocumentProps {
  document: Document;
}

const DocumentItem: FC<DocumentProps> = ({ document }) => {
  return (
    <AnimatedCard
      initial={{ x: -64, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      className="flex items-center justify-between w-full p-5 gap-10"
    >
      <p className="text-lg leading-tight max-w-sm">{document.name}</p>
      <Modal
        title={document.name}
        desc={""}
        Trigger={<Button className="">View</Button>}
      >
        <div className="bg-white py-10 w-full h-1/2 overflow-auto rounded-lg prose">
          <pre>{JSON.stringify(document, null, 2)}</pre>
        </div>
      </Modal>
    </AnimatedCard>
  );
};

DocumentItem.displayName = "DocumentItem";
export default DocumentItem;
