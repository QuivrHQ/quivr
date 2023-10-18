import Link from "next/link";

import { Avatar } from "@/lib/components/ui/Avatar";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import { useGravatar } from "../../../../../hooks/useGravatar";
import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UserButton = (): JSX.Element => {
  const { session } = useSupabase();
  const { gravatarUrl } = useGravatar();

  return (
    <Link aria-label="account" className={sidebarLinkStyle} href={"/user"}>
      <Avatar url={gravatarUrl} alt="user-gravatar" />
      <span className="text-ellipsis overflow-hidden">
        {session?.user.email ?? ""}
      </span>
    </Link>
  );
};
