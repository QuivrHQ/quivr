import { createHash } from "crypto";
import Image from "next/image";
import Link from "next/link";

import { useSupabase } from "@/lib/context/SupabaseProvider";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

// Gravatar images may be requested just like a normal image, using an IMG tag. To get an image specific to a user, you must first calculate their email hash.
// The most basic image request URL looks like this:
// https://www.gravatar.com/avatar/HASH

const computeHash = (email = "") => {
  return createHash("md5")
    .update(typeof email === "string" ? email.trim().toLowerCase() : "")
    .digest("hex");
};

const getGravatarUrl = (email?: string) => {
  const hash = computeHash(email);

  return `https://www.gravatar.com/avatar/${hash}?d=mp`;
};

export const UserButton = (): JSX.Element => {
  const { session } = useSupabase();

  return (
    <Link aria-label="account" className={sidebarLinkStyle} href={"/user"}>
      <div className="relative w-8 h-8">
        <Image
          alt="gravatar"
          layout="fill"
          src={getGravatarUrl(session?.user.email)}
          className="rounded-xl"
        />
      </div>
      <span className="text-ellipsis overflow-hidden">
        {session?.user.email ?? ""}
      </span>
    </Link>
  );
};
