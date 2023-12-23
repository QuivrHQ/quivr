import { LuPanelLeftClose } from "react-icons/lu";

import { Logo } from "@/lib/components/Logo/Logo";
import { useSideBarContext } from "@/lib/context/SidebarProvider/hooks/useSideBarContext";

export const SidebarHeader = (): JSX.Element => {
  const { setIsOpened } = useSideBarContext();

  return (
    <div className="p-2 border-b relative">
      <div className="max-w-screen-xl flex justify-between items-center pt-3 pl-3">
        <Logo />
        <button
          title="Close Sidebar"
          className="p-3 text-2xl bg:white dark:bg-black text-black dark:text-white hover:text-primary dark:hover:text-gray-200 transition-colors"
          type="button"
          data-testid="close-sidebar-button"
          onClick={() => setIsOpened(false)}
        >
          <LuPanelLeftClose />
        </button>
      </div>
    </div>
  );
};
