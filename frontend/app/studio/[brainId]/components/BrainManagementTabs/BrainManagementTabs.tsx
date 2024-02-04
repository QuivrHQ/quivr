/* eslint-disable max-lines */
import { useTranslation } from "react-i18next";

import { StyledTabsTrigger } from "@/app/studio/components/StyledTabsTrigger";
import Button from "@/lib/components/ui/Button";
import Spinner from "@/lib/components/ui/Spinner";
import { Tabs, TabsContent, TabsList } from "@/lib/components/ui/Tabs";

import { KnowledgeOrSecretsTab, PeopleTab, SettingsTab } from "./components";
import { DeleteOrUnsubscribeConfirmationModal } from "./components/Modals/DeleteOrUnsubscribeConfirmationModal";
import { useBrainFetcher } from "./hooks/useBrainFetcher";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";

export const BrainManagementTabs = (): JSX.Element => {
  const { t } = useTranslation([
    "translation",
    "config",
    "delete_or_unsubscribe_from_brain",
    "external_api_definition",
  ]);
  const {
    selectedTab,
    brainId,
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    hasEditRights,
    isPublicBrain,
    isOwnedByCurrentUser,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs();

  const { brain, isLoading } = useBrainFetcher({
    brainId,
  });

  const knowledgeOrSecretsTabLabel =
    brain?.brain_type === "doc"
      ? t("knowledge", { ns: "config" })
      : t("secrets", { ns: "external_api_definition" });

  if (brainId === undefined) {
    return <div />;
  }

  if (isLoading) {
    return (
      <div className="flex w-full h-full justify-center items-center">
        <Spinner />
      </div>
    );
  }

  return (
    <Tabs defaultValue={selectedTab} className="flex flex-col mt-5">
      <TabsList className="flex flex-row justify-center gap-2 border-b-2 rounded-none pb-3">
        <StyledTabsTrigger value="settings">
          {t("settings", { ns: "config" })}
        </StyledTabsTrigger>
        {(!isPublicBrain || hasEditRights) && (
          <>
            <StyledTabsTrigger value="people">
              {t("people", { ns: "config" })}
            </StyledTabsTrigger>
            <StyledTabsTrigger value="knowledgeOrSecrets">
              {knowledgeOrSecretsTabLabel}
            </StyledTabsTrigger>
          </>
        )}
      </TabsList>

      <div className="flex-1 md:pt-0 pb-0">
        <TabsContent value="settings">
          <SettingsTab brainId={brainId} />
        </TabsContent>
        <TabsContent value="people">
          <PeopleTab brainId={brainId} hasEditRights={hasEditRights} />
        </TabsContent>
        <TabsContent value="knowledgeOrSecrets">
          <KnowledgeOrSecretsTab
            brainId={brainId}
            hasEditRights={hasEditRights}
          />
        </TabsContent>
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
    </Tabs>
  );
};
