import Image from "next/image";
import { FC } from "react";
import logo from "../logo.png";
import Link from "next/link";
import Button from "./ui/Button";

interface NavBarProps {}

const NavBar: FC<NavBarProps> = ({}) => {
  return (
    <header className="max-w-screen-xl mx-auto sticky top-0 py-3 flex items-center gap-8 border-b border-b-black/10 dark:border-b-white/25 bg-white">
      <Link href={"/"} className="flex items-center gap-4">
        <Image
          className="rounded-full dark:invert"
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
      <Link href={"/upload"}>
        <Button variant={"secondary"}>Try Demo</Button>
      </Link>
    </header>
  );
};

export default NavBar;
