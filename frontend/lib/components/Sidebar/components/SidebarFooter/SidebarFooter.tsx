import { BrainManagementButton } from "@/lib/components/Sidebar/components/SidebarFooter/components/BrainManagementButton";

import { UpgradeToPlus } from "./components/UpgradeToPlus";
import { UserButton } from "./components/UserButton";

export type SidebarFooterButtons = "myBrains" | "user" | "upgradeToPlus";

type SidebarFooterProps = {
  showButtons: SidebarFooterButtons[];
};

export const SidebarFooter = ({
  showButtons,
}: SidebarFooterProps): JSX.Element => {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 border-t dark:border-white/10 mt-auto p-2">
      <div className="max-w-screen-xl flex justify-center items-center flex-col">
        {showButtons.includes("myBrains") && <BrainManagementButton />}
        {showButtons.includes("upgradeToPlus") && <UpgradeToPlus />}
        {showButtons.includes("user") && <UserButton />}
      </div>
    </div>
  );
};
