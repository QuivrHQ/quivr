"use client";
import Image from "next/image";
import { FC, useEffect, useRef, useState } from "react";
import logo from "../../logo.png";
import Link from "next/link";
import Button from "../ui/Button";
import DarkModeToggle from "./DarkModeToggle";
import { motion } from "framer-motion";

interface NavBarProps {}

const NavBar: FC<NavBarProps> = ({}) => {
  const scrollPos = useRef<number>(0);
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    const handleScroll = (e: Event) => {
      const target = e.currentTarget as Window;
      if (target.scrollY > scrollPos.current && !hidden) {
        setHidden(true);
      } else {
        setHidden(false);
      }
      scrollPos.current = target.scrollY;
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <motion.header
      animate={{
        y: hidden ? "-100%" : "0%",
        transition: { ease: "circOut" },
      }}
      className="fixed top-0 w-full border-b border-b-black/10 dark:border-b-white/25 bg-white dark:bg-black z-50"
    >
      <nav className="max-w-screen-xl mx-auto py-1 flex items-center gap-8">
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
        {process.env.NEXT_PUBLIC_ENV === "local" ? (
          <ul className="flex gap-4 text-sm flex-1">
            <li>
              <Link href={"/upload"}>Upload</Link>
            </li>
            <li>
              <Link href={"/chat"}>Chat</Link>
            </li>
            <li>
              <Link href={"/explore"}>Explore</Link>
            </li>
          </ul>
        ) : (
          <ul className="flex gap-4 text-sm flex-1">
            <li>
              <Link href={"https://github.com/StanGirard/quivr"}>Github</Link>
            </li>
            <li>
              <Link href={"https://discord.gg/HUpRgp2HG8"}>Discord</Link>
            </li>
          </ul>
        )}

        <div className="flex">
          <Link href={"https://try-quivr.streamlit.app"}>
            <Button variant={"secondary"}>Try Demo</Button>
          </Link>
          <DarkModeToggle />
        </div>
      </nav>
    </motion.header>
  );
};

export default NavBar;
