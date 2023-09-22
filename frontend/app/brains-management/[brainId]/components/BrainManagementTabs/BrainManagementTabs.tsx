/* eslint-disable max-lines */
import { Content, List, Root } from "@radix-ui/react-tabs";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainTabTrigger, KnowledgeTab, PeopleTab } from "./components";
import ConfirmationDeleteModal from "./components/Modals/ConfirmationDeleteModal";
import { SettingsTab } from "./components/SettingsTab/SettingsTab";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";
import { isUserBrainOwner } from "./utils/isUserBrainOwner";

export const BrainManagementTabs = (): JSX.Element => {
  const { t } = useTranslation(["translation", "config", "delete_brain"]);
  const {
    selectedTab,
    setSelectedTab,
    brainId,
    handleDeleteBrain,
    isDeleteModalOpen,
    setIsDeleteModalOpen,
    brain,
  } = useBrainManagementTabs();
  const { allBrains } = useBrainContext();

  if (brainId === undefined) {
    return <div />;
  }

  const isCurrentUserBrainOwner = isUserBrainOwner({
    brainId,
    userAccessibleBrains: allBrains,
  });

  const isPublicBrain = brain?.status === "public";

  const hasEditRights = !isPublicBrain || isCurrentUserBrainOwner;

  return (
    <Root
      className="flex flex-col w-full h-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25 p-4 md:p-10"
      value={selectedTab}
    >
      <List
        className="flex flex-col md:flex-row justify-between space-y-2 md:space-y-0 mb-4"
        aria-label={t("subtitle", { ns: "config" })}
      >
        <BrainTabTrigger
          selected={selectedTab === "settings"}
          label={t("settings", { ns: "config" })}
          value="settings"
          onChange={setSelectedTab}
        />
        {hasEditRights && (
          <>
            <BrainTabTrigger
              selected={selectedTab === "people"}
              label={t("people", { ns: "config" })}
              value="people"
              onChange={setSelectedTab}
            />
            <BrainTabTrigger
              selected={selectedTab === "knowledge"}
              label={t("knowledge", { ns: "config" })}
              value="knowledge"
              onChange={setSelectedTab}
            />
          </>
        )}
      </List>

      <div className="flex-1 p-4 md:p-20 md:pt-0">
        <Content value="settings">
          <SettingsTab brainId={brainId} />
        </Content>
        <Content value="people">
          <PeopleTab brainId={brainId} />
        </Content>
        <Content value="knowledge">
          <KnowledgeTab brainId={brainId} />
        </Content>
      </div>

      <div className="flex justify-center mt-4">
        <Button
          disabled={!isCurrentUserBrainOwner}
          className="px-8 md:px-20 py-2 bg-red-500 text-white rounded-md"
          onClick={() => setIsDeleteModalOpen(true)}
        >
          {t("deleteButton", { ns: "delete_brain" })}
        </Button>
      </div>

      <ConfirmationDeleteModal
        isOpen={isDeleteModalOpen}
        setOpen={setIsDeleteModalOpen}
        onDelete={handleDeleteBrain}
      />
    </Root>
  );
};
