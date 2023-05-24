import { cn } from "@/lib/utils";
import Link from "next/link";
import { FC, HTMLAttributes } from "react";
import DarkModeToggle from "./DarkModeToggle";
import Button from "../ui/Button";

interface NavItemsProps extends HTMLAttributes<HTMLUListElement> {}

const NavItems: FC<NavItemsProps> = ({ className, ...props }) => {
  return (
    // <div className={cn("flex flex-1 items-center", className)} {...props}>
    <ul
      className={cn(
        "flex flex-row items-center gap-4 text-sm flex-1",
        className
      )}
      {...props}
    >
      {process.env.NEXT_PUBLIC_ENV === "local" ? (
        <>
          <li>
            <Link href={"/upload"}>Upload</Link>
          </li>
          <li>
            <Link href={"/chat"}>Chat</Link>
          </li>
          <li>
            <Link href={"/explore"}>Explore</Link>
          </li>
        </>
      ) : (
        <>
          <li>
            <Link href={"https://github.com/StanGirard/quivr"}>Github</Link>
          </li>
          <li>
            <Link href={"https://discord.gg/HUpRgp2HG8"}>Discord</Link>
          </li>
        </>
      )}
      <div className="flex sm:flex-1 sm:justify-end flex-col items-center justify-center sm:flex-row gap-5 sm:gap-2">
        <Link href={"https://try-quivr.streamlit.app"}>
          <Button variant={"secondary"}>Try Demo</Button>
        </Link>
        <DarkModeToggle />
      </div>
    </ul>
    // </div>
  );
};

export default NavItems;
