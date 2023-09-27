import { BrainManagementButton } from "@/app/chat/components/ChatsList/components/ChatsListItem/components/BrainManagementButton";

import { UserButton } from "./UserButton";

export const SidebarActions = (): JSX.Element => {
  return (
    <div className="bg-gray-50 dark:bg-gray-900 border-t dark:border-white/10 mt-auto p-2">
      <div className="max-w-screen-xl flex justify-center items-center flex-col">
        <BrainManagementButton />
        <UserButton />
      </div>
    </div>
  );
};
