import { BrainManagementButton } from "@/lib/components/NavBar/components/NavItems/components/BrainManagementButton";

import { UserButton } from "./UserButton";

export const SidebarActions = (): JSX.Element => {
  return (
    <div className="bg-white dark:bg-black border-t dark:border-white/10 mt-auto py-4">
      <div className="max-w-screen-xl mx-auto flex justify-center items-center gap-4 flex-col p-5">
        <BrainManagementButton />
        <UserButton />
      </div>
    </div>
  );
};
