/* eslint-disable max-lines */
import { Content, List, Root } from "@radix-ui/react-tabs";
import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";

import { BrainTabTrigger, KnowledgeTab, PeopleTab } from "./components";
import { DeleteOrUnsubscribeConfirmationModal } from "./components/Modals/DeleteOrUnsubscribeConfirmationModal";
import { SettingsTab } from "./components/SettingsTab/SettingsTab";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";

export const BrainManagementTabs = (): JSX.Element => {
  const { t } = useTranslation([
    "translation",
    "config",
    "delete_or_unsubscribe_from_brain",
  ]);
  const {
    selectedTab,
    setSelectedTab,
    brainId,
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    hasEditRights,
    isOwnedByCurrentUser,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs();

  if (brainId === undefined) {
    return <div />;
  }

  return (
    <div className="flex justify-center w-full">
      <Root
        className="flex flex-col w-full h-full overflow-hidden bg-white dark:bg-black p-4 md:p-10 max-w-5xl"
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

        <div className="flex-1 md:pt-0 pb-0">
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

        <div className="flex justify-center">
          {isOwnedByCurrentUser ? (
            <Button
              className="px-8 md:px-20 py-2 bg-red-500 text-white rounded-md"
              onClick={() => setIsDeleteOrUnsubscribeModalOpened(true)}
            >
              {t("deleteButton", { ns: "delete_or_unsubscribe_from_brain" })}
            </Button>
          ) : (
            <Button
              className="px-8 md:px-20 py-2 bg-red-500 text-white rounded-md"
              onClick={() => setIsDeleteOrUnsubscribeModalOpened(true)}
            >
              {t("unsubscribeButton", {
                ns: "delete_or_unsubscribe_from_brain",
              })}
            </Button>
          )}
        </div>

        <DeleteOrUnsubscribeConfirmationModal
          isOpen={isDeleteOrUnsubscribeModalOpened}
          setOpen={setIsDeleteOrUnsubscribeModalOpened}
          onConfirm={() => void handleUnsubscribeOrDeleteBrain()}
          isOwnedByCurrentUser={isOwnedByCurrentUser}
          isDeleteOrUnsubscribeRequestPending={
            isDeleteOrUnsubscribeRequestPending
          }
        />
      </Root>
    </div>
  );
};
