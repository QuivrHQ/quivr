"use client";
import { AnimatePresence } from "framer-motion";

import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";

import FileComponent from "./components/FileComponent";
import { useFileUploader } from "./hooks/useFileUploader";

export const FileUploader = (): JSX.Element => {
  const {
    getInputProps,
    getRootProps,
    isDragActive,
    isPending,
    open,
    uploadAllFiles,
    files,
    setFiles,
  } = useFileUploader();

  return (
    <section
      {...getRootProps()}
      className="w-full outline-none flex flex-col gap-10 items-center justify-center px-6 py-3"
    >
      <div className="flex flex-col sm:flex-row max-w-3xl w-full items-center gap-5">
        <div className="flex-1 w-full">
          <Card className="h-52 flex justify-center items-center">
            <input {...getInputProps()} />
            <div className="text-center p-6 max-w-sm w-full flex flex-col gap-5 items-center">
              {isDragActive ? (
                <p className="text-blue-600">Drop the files here...</p>
              ) : (
                <button
                  onClick={open}
                  className="opacity-50 h-full cursor-pointer hover:opacity-100 hover:underline transition-opacity"
                >
                  Drag and drop files here, or click to browse
                </button>
              )}
            </div>
          </Card>
        </div>

        {files.length > 0 && (
          <div className="flex-1 w-full">
            <Card className="h-52 py-3 overflow-y-auto">
              {files.length > 0 ? (
                <AnimatePresence mode="popLayout">
                  {files.map((file) => (
                    <FileComponent
                      key={`${file.name} ${file.size}`}
                      file={file}
                      setFiles={setFiles}
                    />
                  ))}
                </AnimatePresence>
              ) : null}
            </Card>
          </div>
        )}
      </div>
      <div className="flex flex-col items-center justify-center">
        <Button isLoading={isPending} onClick={() => void uploadAllFiles()}>
          {isPending ? "Uploading..." : "Upload"}
        </Button>
      </div>
    </section>
  );
};
