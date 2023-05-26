"use client";
import Toast from "@/app/components/ui/Toast";
import { AnimatePresence } from "framer-motion";
import Button from "../../../components/ui/Button";
import Card from "../../../components/ui/Card";
import { FileComponent } from "./components/FileComponent";
import { useFileUploader } from "./hooks/useFileUploader";

export const FileUploader = (): JSX.Element => {
  const {
    getInputProps,
    getRootProps,
    isDragActive,
    isPending,
    messageToast,
    open,
    pendingFileIndex,
    uploadAllFiles,
    files,
    setFiles,
  } = useFileUploader();

  return (
    <>
      <section
        {...getRootProps()}
        className="w-full outline-none flex flex-col gap-5 items-center justify-center p-6"
      >
        <div className="w-full">
          <div className="flex justify-center gap-5">
            {/* Assign a width of 50% to each card */}
            <div className="w-1/2">
              <Card className="h-52 flex justify-center items-center">
                <input {...getInputProps()} />
                <div className="text-center mt-2 p-6 max-w-sm w-full flex flex-col gap-5 items-center">
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
              <div className="w-1/2">
                <Card className="h-52 py-3 overflow-y-auto">
                  {files.length > 0 ? (
                    <AnimatePresence>
                      {files.map((file) => (
                        <FileComponent
                          key={file.name + file.size}
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
          <div className="flex flex-col items-center justify-center mt-5">
            <Button isLoading={isPending} onClick={uploadAllFiles}>
              {isPending
                ? `Uploading ${files[pendingFileIndex].name}`
                : "Upload"}
            </Button>
          </div>
        </div>
      </section>
      <Toast ref={messageToast} />
    </>
  );
};
