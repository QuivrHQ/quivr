"use client";
import { useAxios } from "@/lib/useAxios";
import { AnimatePresence, motion } from "framer-motion";
import Link from "next/link";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import Button from "../components/ui/Button";
import Spinner from "../components/ui/Spinner";
import { useSupabase } from "../supabase-provider";
import DocumentItem from "./DocumentItem";
import { Document } from "./types";

export default function ExplorePage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isPending, setIsPending] = useState(true);
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();

  if (session === null) {
    redirect("/login");
  }

  useEffect(() => {
    const fetchDocuments = async () => {
      setIsPending(true);
      try {
        console.log(
          `Fetching documents from ${process.env.NEXT_PUBLIC_BACKEND_URL}/explore`
        );
        const response = await axiosInstance.get<{ documents: Document[] }>(
          "/explore"
        );
        setDocuments(response.data.documents);
      } catch (error) {
        console.error("Error fetching documents", error);
        setDocuments([]);
      }
      setIsPending(false);
    };
    fetchDocuments();
  }, [session.access_token]);

  return (
    <main>
      <section className="w-full outline-none pt-32 flex flex-col gap-5 items-center justify-center p-6">
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-3xl font-bold text-center">
            Explore uploaded data
          </h1>
          <h2 className="opacity-50">
            View or delete stored data used by your brain
          </h2>
        </div>
        {isPending ? (
          <Spinner />
        ) : (
          <motion.div layout className="w-full max-w-xl flex flex-col gap-5">
            {documents.length !== 0 ? (
              <AnimatePresence mode="popLayout">
                {documents.map((document) => (
                  <DocumentItem
                    key={document.name}
                    document={document}
                    setDocuments={setDocuments}
                  />
                ))}
              </AnimatePresence>
            ) : (
              <div className="flex flex-col items-center justify-center mt-10 gap-1">
                <p className="text-center">Oh No, Your Brain is empty.</p>
                <Link href="/upload">
                  <Button>Upload</Button>
                </Link>
              </div>
            )}
          </motion.div>
        )}
      </section>
    </main>
  );
}
