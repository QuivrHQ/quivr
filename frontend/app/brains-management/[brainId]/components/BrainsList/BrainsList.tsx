"use client";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { Sidebar } from "@/lib/components/Sidebar/Sidebar";
import Button from "@/lib/components/ui/Button";

import { BrainListItem } from "./components/BrainListItem";
import { BrainSearchBar } from "./components/BrainSearchBar";
import { useBrainsList } from "./hooks/useBrainsList";

export const BrainsList = (): JSX.Element => {
  const { searchQuery, setSearchQuery, brains, isOnBrainsLibraryPage } =
    useBrainsList();

  const { t } = useTranslation(["brain", "chat"]);

  return (
    <Sidebar showButtons={["upgradeToPlus", "user"]}>
      <div className="flex flex-col p-2 gap-2">
        <Link href="/chat">
          <Button type="button" className="bg-primary text-white py-2 w-full">
            {t("chat:back_to_chat")}
          </Button>
        </Link>
        <AddBrainModal triggerClassName="border-solid border-2 border-gray-300" />
      </div>
      <div className="px-2 pt-2 pb-4">
        <BrainSearchBar
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />
      </div>
      <div
        data-testid="brains-list-items"
        className="flex-1 overflow-auto scrollbar h-full min-h-[50px]"
      >
        {brains.map((brain) => (
          <BrainListItem brain={brain} key={brain.id} />
        ))}
      </div>
      <div className="p-2 mb flex flex-col">
        {isOnBrainsLibraryPage ? (
          <Link href="/brains-management" className="flex flex-row flex-1">
            <Button
              type="button"
              className="bg-primary text-white py-2 mb-2 flex flex-row flex-1"
            >
              {t("brain:brain_management_button_label")}
            </Button>
          </Link>
        ) : (
          <Link href="/brains-management/library">
            <Button type="button" className="bg-primary text-white py-2 w-full">
              {t("brain_library_button_label")}
            </Button>
          </Link>
        )}
      </div>
    </Sidebar>
  );
};
