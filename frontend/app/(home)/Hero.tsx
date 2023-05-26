"use client";
import { motion, useScroll, useSpring, useTransform } from "framer-motion";
import Link from "next/link";
import { FC, useRef } from "react";
import { MdNorthEast } from "react-icons/md";
import Button from "../components/ui/Button";

const Hero: FC = () => {
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
          Get a Second Brain with <span className="text-primary">Quivr</span>
        </h1>
        <p className="text-base max-w-sm text-gray-500 mb-5 sm:mb-10">
          Quivr is your second brain in the cloud, designed to easily store and
          retrieve unstructured information.
        </p>
        <Link href={"https://try-quivr.streamlit.app"}>
          <Button>Try Demo</Button>
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
        src="https://user-images.githubusercontent.com/19614572/238774100-80721777-2313-468f-b75e-09379f694653.mp4"
        autoPlay
        muted
        loop
      />
    </section>
  );
};

export default Hero;
