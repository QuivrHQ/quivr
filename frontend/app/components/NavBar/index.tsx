import Image from "next/image";
import { FC } from "react";
import logo from "../../logo.png";
import Link from "next/link";
import Button from "../ui/Button";
import DarkModeToggle from "./DarkModeToggle";

interface NavBarProps {}

const NavBar: FC<NavBarProps> = ({}) => {
  return (
    <header className="sticky top-0 border-b border-b-black/10 dark:border-b-white/25 bg-white/50 dark:bg-black/50 bg-opacity-0 backdrop-blur-md z-50">
      <nav className="max-w-screen-xl mx-auto py-3 flex items-center gap-8">
        <Link href={"/"} className="flex items-center gap-4">
          <Image
            className="rounded-full"
            src={logo}
            alt="Quivr Logo"
            width={48}
            height={48}
          />
          <h1 className="font-bold">Quivr</h1>
        </Link>
        <ul className="flex gap-4 text-sm flex-1">
          <li>
            <Link href="/#features">Features</Link>
          </li>
          <li>
            <Link href="/chat">Chat</Link>
          </li>
          <li>
            <Link href="/upload">Demo</Link>
          </li>
        </ul>
        <div className="flex">
          <Link href={"/upload"}>
            <Button variant={"secondary"}>Try Demo</Button>
          </Link>
          <DarkModeToggle />
        </div>
      </nav>
    </header>
  );
};

export default NavBar;
