import Link from "next/link";
import { MdPerson } from "react-icons/md";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UserButton = (): JSX.Element => {
  const { session } = useSupabase();

  return (
    <Link aria-label="account" className={sidebarLinkStyle} href={"/user"}>
      <MdPerson className="text-4xl" />
      <span className="text-ellipsis overflow-hidden">
        {session?.user.email ?? ""}
      </span>
    </Link>
  );
};
