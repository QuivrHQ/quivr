"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import DocumentItem from "./DocumentItem";
import { Document } from "./types";
import Button from "../components/ui/Button";
import Link from "next/link";
import Spinner from "../components/ui/Spinner";

export default function ExplorePage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isPending, setIsPending] = useState(true);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setIsPending(true);
    try {
      console.log(
        `Fetching documents from ${process.env.NEXT_PUBLIC_BACKEND_URL}/explore`
      );
      const response = await axios.get<{ documents: Document[] }>(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/explore`
      );
      setDocuments(response.data.documents);
    } catch (error) {
      console.error("Error fetching documents", error);
      setDocuments([]);
    }
    setIsPending(false);
  };

  return (
    <div className="pt-20 flex flex-col items-center justify-center p-6">
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-3xl font-bold text-center">Explore Your Brain</h1>
        <h2 className="opacity-50">View what&rsquo;s in your second brain</h2>
      </div>
      {isPending ? (
        <Spinner />
      ) : (
        <div className="w-full max-w-xl flex flex-col gap-5">
          {documents.length !== 0 ? (
            documents.map((document, index) => (
              <DocumentItem
                key={index}
                document={document}
                setDocuments={setDocuments}
              />
            ))
          ) : (
            <div className="flex flex-col items-center justify-center mt-10 gap-1">
              <p className="text-center">Oh No, Your Brain is empty.</p>
              <Link href="/upload">
                <Button>Upload Files</Button>
              </Link>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
