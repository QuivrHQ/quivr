import Link from "next/link";
import { FiUser } from "react-icons/fi";

import { useUserData } from "@/lib/hooks/useUserData";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UpgradeToPlus = (): JSX.Element => {
  const { userData } = useUserData();
  const is_premium = userData?.is_premium;

  if (is_premium === true) {
    return <></>;
  }

  return (
    <Link href="/" className={sidebarLinkStyle}>
      <FiUser className="w-8 h-8" />
      <span>
        Upgrade to plus{" "}
        <span className="rounded bg-primary/80 py-1 px-3 text-xs">New</span>
      </span>
    </Link>
  );
};
