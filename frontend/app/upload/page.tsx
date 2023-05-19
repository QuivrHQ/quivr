"use client";
import { Dispatch, SetStateAction, useCallback, useState } from "react";
import { FileRejection, useDropzone } from "react-dropzone";
import axios from "axios";
import { Message } from "@/lib/types";
import Button from "../components/ui/Button";
import { MdClose } from "react-icons/md";
import { AnimatePresence, motion } from "framer-motion";
import Link from "next/link";

export default function UploadPage() {
  const [message, setMessage] = useState<Message | null>(null);
  const [files, setFiles] = useState<File[]>([]);

  const upload = useCallback(async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData
      );
      console.log(response.data.message);

      setMessage({
        type: "success",
        text:
          "File uploaded successfully: " +
          JSON.stringify(response.data.message),
      });
    } catch (error: any) {
      setMessage({
        type: "error",
        text: "Failed to upload file: " + error.toString(),
      });
    }
  }, []);

  const onDrop = (acceptedFiles: File[], fileRejections: FileRejection[]) => {
    if (fileRejections.length > 0) {
      setMessage({ type: "error", text: "File too big." });
      return;
    }
    setMessage(null);
    for (let i = 0; i < acceptedFiles.length; i++) {
      const file = acceptedFiles[i];
      const isAlreadyInFiles =
        files.filter((f) => f.name === file.name && f.size === file.size)
          .length > 0;
      if (isAlreadyInFiles) {
        setMessage({ type: "warning", text: `${file.name} was already added` });
        acceptedFiles.splice(i, 1);
      }
    }
    setFiles((files) => [...files, ...acceptedFiles]);
  };

  const { getRootProps, getInputProps, isDragActive, open } = useDropzone({
    onDrop,
    noClick: true,
    maxSize: 1000000, // 1 MB
  });

  return (
    <main>
      <section
        {...getRootProps()}
        className="w-full h-full min-h-screen text-center flex flex-col items-center gap-5 pt-32 outline-none"
      >
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-5xl font-bold">Add Knowledge</h1>
          <h2 className="opacity-50">Upload files to your second brain</h2>
        </div>
        <div className="shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25">
          <input {...getInputProps()} />
          <div className="text-center mt-2 p-6 max-w-sm w-full flex flex-col gap-5 items-center">
            {files.length > 0 ? (
              <AnimatePresence>
                {files.map((file, i) => (
                  <FileComponent
                    key={file.name + file.size}
                    file={file}
                    setFiles={setFiles}
                  />
                ))}
              </AnimatePresence>
            ) : null}

            {isDragActive ? (
              <p className="text-blue-600">Drop the files here...</p>
            ) : (
              <button
                onClick={open}
                className="opacity-50 cursor-pointer hover:opacity-100 hover:underline transition-opacity"
              >
                Drag and drop some files here, or click to browse files
              </button>
            )}
          </div>
          {message && (
            <div
              className={`mt-4 p-6 max-w-sm rounded ${
                message.type === "success"
                  ? "bg-green-500"
                  : message.type === "warning"
                  ? "bg-yellow-600"
                  : "bg-red-500"
              }`}
            >
              <p className="text-white">{message.text}</p>
            </div>
          )}
        </div>
        <p className="opacity-50">
          This is the demo mode, the max file size is 1MB
        </p>
        <div className="flex gap-5">
          <Link href={"/chat"}>
            <Button variant={"secondary"} className="py-3">
              Start Chatting with your brain
            </Button>
          </Link>
          <Button
            onClick={() => {
              files.forEach((file) => upload(file));
            }}
            className=""
          >
            Add
          </Button>
        </div>
      </section>
    </main>
  );
}

const FileComponent = ({
  file,
  setFiles,
}: {
  file: File;
  setFiles: Dispatch<SetStateAction<File[]>>;
}) => {
  return (
    <motion.div
      initial={{ x: "-10%", opacity: 0 }}
      animate={{ x: "0%", opacity: 1 }}
      exit={{ x: "10%", opacity: 0 }}
      className="flex py-2 dark:bg-black border-b border-black/10 dark:border-white/25 w-full text-left leading-none"
    >
      <div className="flex flex-col gap-1 flex-1">
        <span className="flex-1 mr-10">{file.name}</span>
        <span className="text-xs opacity-50">
          {(file.size / 1000).toFixed(3)} kb
        </span>
      </div>
      <button
        role="remove file"
        className="ml-5 text-xl text-red-500 px-5"
        onClick={() =>
          setFiles((files) =>
            files.filter((f) => f.name !== file.name || f.size !== file.size)
          )
        }
      >
        <MdClose />
      </button>
    </motion.div>
  );
};
