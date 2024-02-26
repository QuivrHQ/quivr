/* eslint-disable max-lines */
import { useTranslation } from "react-i18next";

import { StyledTabsTrigger } from "@/app/studio/components/StyledTabsTrigger";
import Spinner from "@/lib/components/ui/Spinner";
import { Tabs, TabsContent, TabsList } from "@/lib/components/ui/Tabs";

import { KnowledgeOrSecretsTab, PeopleTab, SettingsTab } from "./components";
import { useBrainFetcher } from "./hooks/useBrainFetcher";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";

export const BrainManagementTabs = (): JSX.Element => {
  const { t } = useTranslation([
    "translation",
    "config",
    "delete_or_unsubscribe_from_brain",
    "external_api_definition",
  ]);
  const { selectedTab, brainId, hasEditRights } = useBrainManagementTabs();

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
        {hasEditRights && (
          <>
            <StyledTabsTrigger value="people">
              {t("people", { ns: "config" })}
            </StyledTabsTrigger>
            {brain?.brain_type === "doc" && (
              <StyledTabsTrigger value="knowledgeOrSecrets">
                {knowledgeOrSecretsTabLabel}
              </StyledTabsTrigger>
            )}
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
        {brain?.brain_type === "doc" && (
          <TabsContent value="knowledgeOrSecrets">
            <KnowledgeOrSecretsTab
              brainId={brainId}
              hasEditRights={hasEditRights}
            />
          </TabsContent>
        )}
      </div>
    </Tabs>
  );
};
