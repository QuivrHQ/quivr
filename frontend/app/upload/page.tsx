"use client";
import Link from "next/link";
import { Suspense } from "react";
import { useTranslation } from "react-i18next";

import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";
import PageHeading from "@/lib/components/ui/PageHeading";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";

const requiredRolesForUpload: BrainRoleType[] = ["Editor", "Owner"];

const UploadPage = (): JSX.Element => {
  const { currentBrain } = useBrainContext();
  const { session } = useSupabase();
  const { t } = useTranslation(["translation", "upload"]);

  if (session === null) {
    redirectToLogin();
  }

  if (currentBrain === undefined) {
    return (
      <div className="flex justify-center items-center mt-5">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md">
          <strong className="font-bold mr-1">
            {t("ohNo", { ns: "upload" })}
          </strong>
          <span className="block sm:inline">
            {t("selectBrainFirst", { ns: "upload" })}
          </span>
        </div>
      </div>
    );
  }

  const hasUploadRights = requiredRolesForUpload.includes(currentBrain.role);

  if (!hasUploadRights) {
    return (
      <div className="flex justify-center items-center mt-5">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md">
          <strong className="font-bold mr-1">
            {t("ohNo", { ns: "upload" })}
          </strong>
          <span className="block sm:inline">
            {t("missingNecessaryRole", { ns: "upload" })}
          </span>
        </div>
      </div>
    );
  }

  const Upload = () => {
    return (
      <main className="pt-10">
        <PageHeading
          title={t("title", { ns: "upload" })}
          subtitle={t("subtitle", { ns: "upload" })}
        />
        <FileUploader />
        <Divider text={t("or")} className="m-5" />
        <Crawler />
        <div className="flex flex-col items-center justify-center gap-5 mt-5">
          <Link href={"/chat"}>
            <Button variant={"secondary"} className="py-3">
              {t("chatButton")}
            </Button>
          </Link>
        </div>
      </main>
    );
  };

  return (
    <Suspense fallback="Loading...">
      <Upload />
    </Suspense>
  );
};

export default UploadPage;
