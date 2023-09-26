import Link from "next/link";
import { MdPerson } from "react-icons/md";

import { useUserData } from "@/lib/hooks/useUserData";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UserButton = (): JSX.Element => {
  const { userData } = useUserData();

  return (
    <Link aria-label="account" className={sidebarLinkStyle} href={"/user"}>
      <MdPerson className="text-4xl" />
      <span>{userData?.email}</span>
    </Link>
  );
};
