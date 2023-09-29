"use client";
import { motion, MotionConfig } from "framer-motion";
import Link from "next/link";
import { useTranslation } from "react-i18next";

import { AddBrainModal } from "@/lib/components/AddBrainModal/AddBrainModal";
import Button from "@/lib/components/ui/Button";
import { cn } from "@/lib/utils";

import { BrainListDisplayToggleButton } from "./components/BrainListDisplayToggleButton/BrainListDisplayToggleButton";
import { BrainListItem } from "./components/BrainListItem";
import { BrainSearchBar } from "./components/BrainSearchBar";
import { useBrainsList } from "./hooks/useBrainsList";

export const BrainsList = (): JSX.Element => {
  const {
    opened,
    setOpened,
    searchQuery,
    setSearchQuery,
    brains,
    isOnBrainsLibraryPage,
  } = useBrainsList();

  const { t } = useTranslation("brain");

  return (
    <MotionConfig transition={{ massq: 1, damping: 10 }}>
      <motion.div
        drag="x"
        dragConstraints={{ right: 0, left: 0 }}
        dragElastic={0.15}
        onDragEnd={(event, info) => {
          if (info.offset.x > 100 && !opened) {
            setOpened(true);
          } else if (info.offset.x < -100 && opened) {
            setOpened(false);
          }
        }}
        className="flex flex-col lg:sticky fixed top-16 left-0 bottom-0 lg:h-[90vh] overflow-visible z-30 border-r border-black/10 dark:border-white/25 bg-white dark:bg-black"
      >
        <motion.div
          animate={{
            width: opened ? "fit-content" : "0px",
            opacity: opened ? 1 : 0.5,
            boxShadow: opened
              ? "10px 10px 16px rgba(0, 0, 0, 0)"
              : "10px 10px 16px rgba(0, 0, 0, 0.5)",
          }}
          className={cn("overflow-hidden flex flex-col flex-1")}
          data-testid="brains-list"
        >
          <div className="flex flex-col flex-1">
            <BrainSearchBar
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
            />
            <div
              data-testid="brains-list-items"
              className="flex-1 overflow-auto scrollbar h-full"
            >
              {brains.map((brain) => (
                <BrainListItem brain={brain} key={brain.id} />
              ))}
            </div>
            <div className="m-2 mb flex flex-col">
              {isOnBrainsLibraryPage ? (
                <Link
                  href="/brains-management"
                  className="flex flex-row flex-1"
                >
                  <Button
                    type="button"
                    className="bg-primary text-white py-2 mb-2 flex flex-row flex-1"
                  >
                    {t("brain_management_button_label")}
                  </Button>
                </Link>
              ) : (
                <Link
                  href="/brains-management/library"
                  className="flex flex-row flex-1"
                >
                  <Button
                    type="button"
                    className="bg-primary text-white py-2 mb-2 flex flex-row flex-1"
                  >
                    {t("brain_library_button_label")}
                  </Button>
                </Link>
              )}
              <AddBrainModal triggerClassName="border-solid border-2 border-gray-300" />
            </div>
          </div>
        </motion.div>
        <BrainListDisplayToggleButton opened={opened} setOpened={setOpened} />
      </motion.div>
    </MotionConfig>
  );
};
