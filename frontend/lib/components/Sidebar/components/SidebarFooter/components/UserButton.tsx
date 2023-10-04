import Image from "next/image";
import Link from "next/link";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { useGravatar } from "../../../../../hooks/useGravatar";
import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UserButton = (): JSX.Element => {
  const { session } = useSupabase();
  const { gravatarUrl } = useGravatar();

  return (
    <Link aria-label="account" className={sidebarLinkStyle} href={"/user"}>
      <div className="relative w-8 h-8">
        <Image
          alt="gravatar"
          fill={true}
          sizes="32px"
          src={gravatarUrl}
          className="rounded-xl"
        />
      </div>
      <span className="text-ellipsis overflow-hidden">
        {session?.user.email ?? ""}
      </span>
    </Link>
  );
};
