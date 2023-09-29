import { Dispatch, SetStateAction } from "react";
import { LuPanelLeft } from "react-icons/lu";

import { Logo } from "@/lib/components/NavBar/components/Logo";

type SidebarProps = {
  setOpen: Dispatch<SetStateAction<boolean>>;
};

export const SidebarHeader = ({ setOpen }: SidebarProps): JSX.Element => {
  return (
    <div className="p-2 border-b relative">
      <div className="max-w-screen-xl flex justify-between items-center pt-3 pl-3">
        <Logo />
        <button
          title="Close Sidebar"
          className="p-3 text-2xl bg:white dark:bg-black text-black dark:text-white hover:text-primary dark:hover:text-gray-200 transition-colors"
          type="button"
          data-testid="close-sidebar-button"
          onClick={() => setOpen(false)}
        >
          <LuPanelLeft />
        </button>
      </div>
    </div>
  );
};
