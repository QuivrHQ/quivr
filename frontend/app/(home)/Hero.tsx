"use client";
import { motion, useScroll, useSpring, useTransform } from "framer-motion";
import Link from "next/link";
import { useRef } from "react";
import { useTranslation } from "react-i18next";
import { MdNorthEast } from "react-icons/md";

import Button from "@/lib/components/ui/Button";

const Hero = (): JSX.Element => {
  const { t } = useTranslation();

  const targetRef = useRef<HTMLDivElement | null>(null);
  const { scrollYProgress } = useScroll({
    target: targetRef,
    offset: ["start start", "end start"],
  });

  const scaleSync = useTransform(scrollYProgress, [0, 0.5], [1, 0.9]);
  const scale = useSpring(scaleSync, { mass: 0.1, stiffness: 100 });

  const position = useTransform(scrollYProgress, (pos) => {
    if (pos === 1) {
      return "relative";
    }

    return "sticky";
  });

  const videoScaleSync = useTransform(scrollYProgress, [0, 0.5], [0.9, 1]);
  const videoScale = useSpring(videoScaleSync, { mass: 0.1, stiffness: 100 });

  const opacitySync = useTransform(scrollYProgress, [0, 0.5], [1, 0]);
  const opacity = useSpring(opacitySync, { mass: 0.1, stiffness: 200 });

  return (
    <section
      ref={targetRef}
      className="relative w-full flex flex-col gap-24 items-center text-center min-h-[768px] py-12"
    >
      <motion.div
        style={{ scale, opacity, position }}
        className="top-24 -z-0 flex flex-col gap-2 items-center justify-center pt-24"
      >
        <h1 className="text-5xl sm:text-7xl font-bold max-w-lg sm:max-w-xl">
         {t("title.short")} <span className="text-primary">Quivr</span>
        </h1>
        <p className="text-base max-w-sm text-gray-500 mb-5 sm:mb-10">
          {t("description")}
        </p>
        <Link href={"/login"}>
          <Button>{t("getStarted")}</Button>
        </Link>
        <Link target="_blank" href={"https://github.com/StanGirard/quivr/"}>
          <Button variant={"tertiary"}>
            Github <MdNorthEast />
          </Button>
        </Link>
      </motion.div>
      <motion.video
        style={{ scale: videoScale }}
        className="rounded-md max-w-screen-lg shadow-lg dark:shadow-white/25 border dark:border-white/25 w-full bg-white dark:bg-black"
        src="https://user-images.githubusercontent.com/19614572/239713902-a6463b73-76c7-4bc0-978d-70562dca71f5.mp4"
        autoPlay
        muted
        loop
      />
    </section>
  );
};

export default Hero;
