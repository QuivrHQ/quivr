"use client";

import { useTranslation } from "react-i18next";
import { LuBrain, LuChevronLeftCircle } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

import { BrainManagementTabs } from "./components";
import { useBrainManagement } from "./hooks/useBrainManagement";

const BrainsManagement = (): JSX.Element => {
  const { t } = useTranslation(["translation"]);
  const { brain } = useBrainManagement();

  return (
    <div className="flex flex-col w-full p-10 bg-highlight">
      <div>
        <Button variant={"tertiary"}>
          <LuChevronLeftCircle className="text-primary" />
          {t("previous")}
        </Button>
      </div>
      <div className="w-full justify-center flex items-center gap-2">
        <LuBrain size={25} className="text-primary" />
        <span className="text-3xl font-semibold">{brain?.name}</span>
      </div>
      <BrainManagementTabs />
    </div>
  );
};

export default BrainsManagement;
