import Link from "next/link";
import { MdPerson } from "react-icons/md";

import { BrainManagementButton } from "@/lib/components/NavBar/components/NavItems/components/BrainManagementButton";

export const SidebarActions = (): JSX.Element => {
  return (
    <div className="bg-white dark:bg-black border-t dark:border-white/10 mt-auto py-4">
      <div className="max-w-screen-xl mx-auto flex justify-center items-center gap-4 flex-col">
        <BrainManagementButton />
        <Link aria-label="account" className="" href={"/user"}>
          <MdPerson className="text-2xl" />
        </Link>
      </div>
    </div>
  );
};
