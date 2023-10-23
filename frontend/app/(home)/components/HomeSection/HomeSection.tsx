import { cn } from "@/lib/utils";

import styles from "./HomeSection.module.css";

type HomeSectionProps = {
  bg: string;
  slantCurrent?: "up" | "down" | "none";
  slantBefore?: "up" | "down" | "none";
  slantAfter?: "up" | "down" | "none";
  gradient?: string;
  hiddenOnMobile?: boolean;
  children: React.ReactNode;
  className?: string;
};

export const HomeSection = ({
  bg,
  slantCurrent = "none",
  slantBefore = "none",
  slantAfter = "none",
  gradient,
  hiddenOnMobile = false,
  className,
  children,
}: HomeSectionProps): JSX.Element => {
  const slantBeforeFix = styles[`slant-before-is-${slantBefore}`] ?? "";
  const slantAfterFix = styles[`slant-after-is-${slantAfter}`] ?? "";
  const flex = hiddenOnMobile
    ? "hidden md:flex md:justify-center"
    : "flex justify-center";
  const slant = styles[`section-slanted-${slantCurrent}wards`] ?? "";

  return (
    <div
      className={cn(
        `${bg} w-screen ${flex} ${slantBeforeFix} ${slantAfterFix} ${slant} overflow-hidden`,
        className
      )}
    >
      <section className="flex flex-col items-center w-full max-w-6xl z-[2] py-8">
        {children}
      </section>
      {gradient !== undefined ? (
        <div
          className={`absolute w-screen bottom-[calc(100vw*tan(6deg))] left-0 h-[30%] ${gradient}`}
        />
      ) : null}
    </div>
  );
};
