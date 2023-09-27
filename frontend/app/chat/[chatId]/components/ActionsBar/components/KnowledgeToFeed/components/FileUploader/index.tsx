"use client";
import { useTranslation } from "react-i18next";
import { IoCloudUploadOutline } from "react-icons/io5";

import Card from "@/lib/components/ui/Card";

import { useFileUploader } from "./hooks/useFileUploader";
import { FeedItemType } from "../../../../types";

type FileUploaderProps = {
  addContent: (content: FeedItemType) => void;
  files: File[];
};
export const FileUploader = ({
  addContent,
  files,
}: FileUploaderProps): JSX.Element => {
  const { getInputProps, getRootProps, isDragActive, open } = useFileUploader({
    addContent,
    files,
  });

  const { t } = useTranslation(["translation", "upload"]);

  return (
    <section
      {...getRootProps()}
      className="w-full outline-none flex flex-col gap-10 items-center justify-center px-6 py-3"
    >
      <div className="flex flex-col sm:flex-row max-w-3xl w-full items-center gap-5">
        <div className="flex-1 w-full">
          <Card className="h-24 flex justify-center items-center">
            <IoCloudUploadOutline className="relative right-16 text-5xl" />
            <input {...getInputProps()} />
            <div className="text-center p-6 max-w-sm w-full flex flex-col gap-5 items-center">
              {isDragActive ? (
                <p className="text-blue-600">{t("drop", { ns: "upload" })}</p>
              ) : (
                <button
                  onClick={open}
                  className="opacity-50 h-full cursor-pointer hover:opacity-100 hover:underline transition-opacity"
                >
                  {t("dragAndDrop", { ns: "upload" })}
                </button>
              )}
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};
