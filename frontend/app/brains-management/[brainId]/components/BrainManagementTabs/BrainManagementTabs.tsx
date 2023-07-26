import { Content, List, Root } from "@radix-ui/react-tabs";

import { BrainTabTrigger, PeopleTab } from "./components";
import { SettingsTab } from "./components/SettingsTab/SettingsTab";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";

export const BrainManagementTabs = (): JSX.Element => {
  const { selectedTab, setSelectedTab, brainId } = useBrainManagementTabs();

  if (brainId === undefined) {
    return <div />;
  }

  return (
    <Root
      className="shadow-md min-h-[50%] dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25 p-4 pt-10"
      defaultValue="settings"
    >
      <List className="flex justify-between" aria-label="Manage your brain">
        <BrainTabTrigger
          selected={selectedTab === "settings"}
          label="Settings"
          value="settings"
          onChange={setSelectedTab}
        />
        <BrainTabTrigger
          selected={selectedTab === "people"}
          label="People"
          value="people"
          onChange={setSelectedTab}
        />
        <BrainTabTrigger
          selected={selectedTab === "knowledge"}
          label="Knowledge"
          value="knowledge"
          onChange={setSelectedTab}
        />
      </List>

      <div className="p-20 pt-5">
        <Content value="settings">
          <SettingsTab brainId={brainId} />
        </Content>
        <Content value="people">
          <PeopleTab brainId={brainId} />
        </Content>
        <Content value="knowledge">
          <p>Coming soon</p>
        </Content>
      </div>
    </Root>
  );
};
