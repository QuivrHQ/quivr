"use client";

import { useTranslation } from "react-i18next";
import { LuBrain } from "react-icons/lu";

import { AddBrainModal } from "@/lib/components/AddBrainModal";

import { BrainsTabs } from "./components/BrainsTabs/BrainsTabs";

const BrainsManagement = (): JSX.Element => {
  const { t } = useTranslation("chat");

  return (
    <div className="flex flex-col flex-1 bg-white">
      <div className="w-full h-full p-6 flex flex-col flex-1 overflow-auto">
        <div className="w-full mb-10">
          <div className="flex flex-row justify-center items-center gap-2">
            <LuBrain size={20} className="text-primary" />
            <span className="capitalize text-2xl font-semibold">
              {t("brains")}
            </span>
          </div>
        </div>
        <BrainsTabs />
      </div>
      <div className="w-full flex justify-center py-4">
        <AddBrainModal />
      </div>
    </div>
  );
};

export default BrainsManagement;
