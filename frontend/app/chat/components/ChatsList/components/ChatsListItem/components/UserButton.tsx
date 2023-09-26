import Link from "next/link";
import { MdPerson } from "react-icons/md";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UserButton = (): JSX.Element => {
  return (
    <Link aria-label="account" className={sidebarLinkStyle} href={"/user"}>
      <MdPerson className="text-4xl" />
      <span>Account</span>
    </Link>
  );
};
