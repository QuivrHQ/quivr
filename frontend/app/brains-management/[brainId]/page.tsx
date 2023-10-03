"use client";

import { UUID } from "crypto";
import { useParams } from "next/navigation";
import { useTranslation } from "react-i18next";

import { BrainManagementTabs } from "./components";

const BrainsManagement = (): JSX.Element => {
  const params = useParams();
  const { t } = useTranslation(["brain"]);

  const brainId = params?.brainId as UUID | undefined;

  if (brainId === undefined) {
    return (
      <div className="flex justify-center mt-5 w-full">
        <div className="bg-blue-100 border border-blue-400 text-blue-700 px-4 py-3 rounded relative max-w-md h-fit">
          <p>{t("selectBrain")}</p>
        </div>
      </div>
    );
  }

  return <BrainManagementTabs />;
};

export default BrainsManagement;
