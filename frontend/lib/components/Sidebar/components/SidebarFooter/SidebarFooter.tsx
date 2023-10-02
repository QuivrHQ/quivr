import { BrainManagementButton } from "@/lib/components/Sidebar/components/SidebarFooter/components/BrainManagementButton";

import { UserButton } from "./components/UserButton";

export const SidebarFooter = (): JSX.Element => {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 border-t dark:border-white/10 mt-auto p-2">
      <div className="max-w-screen-xl flex justify-center items-center flex-col">
        <BrainManagementButton />
        <UserButton />
      </div>
    </div>
  );
};
