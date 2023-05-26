"use client";
import Image from "next/image";
import { FC, useEffect, useRef, useState } from "react";

import { motion } from "framer-motion";
import Link from "next/link";
import MobileMenu from "./MobileMenu";
import NavItems from "./NavItems";

const NavBar: FC = () => {
  const scrollPos = useRef<number>(0);
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    const handleScroll = (e: Event) => {
      const target = e.currentTarget as Window;
      if (target.scrollY > scrollPos.current) {
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
      className="fixed top-0 w-full border-b border-b-black/10 dark:border-b-white/25 bg-white dark:bg-black z-20"
    >
      <nav className="max-w-screen-xl mx-auto py-1 flex items-center justify-between gap-8">
        <Link href={"/"} className="flex items-center gap-4">
          <Image
            className="rounded-full"
            src={"/logo.png"}
            alt="Quivr Logo"
            width={48}
            height={48}
          />
          <h1 className="font-bold">Quivr</h1>
        </Link>
        <NavItems className="hidden sm:flex" />
        <MobileMenu />
      </nav>
    </motion.header>
  );
};

export default NavBar;
