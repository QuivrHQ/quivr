"use client";
import { useTranslation } from "react-i18next";
import { IoCloudUploadOutline } from "react-icons/io5";

import Card from "@/lib/components/ui/Card";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useCustomDropzone } from "@/lib/hooks/useDropzone";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

export const FileUploader = (): JSX.Element => {
  const { session } = useSupabase();
  const { getInputProps, isDragActive, open } = useCustomDropzone();

  if (session === null) {
    redirectToLogin();
  }

  const { t } = useTranslation(["translation", "upload"]);

  return (
    <section className="w-full outline-none flex flex-col gap-10 items-center justify-center px-0">
      <div className="flex flex-col sm:flex-row max-w-3xl w-full items-center gap-5 cursor-pointer">
        <div className="flex-1 w-full">
          <Card
            className="h-20 flex justify-center items-center"
            onClick={open}
          >
            <IoCloudUploadOutline className="text-5xl" />
            <input {...getInputProps()} />
            {isDragActive && (
              <p className="text-blue-600">{t("drop", { ns: "upload" })}</p>
            )}
          </Card>
        </div>
      </div>
    </section>
  );
};
