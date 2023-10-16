import styles from "./HomeSection.module.css";

type HomeSectionProps = {
  bg: string;
  slantCurrent?: "up" | "down" | "none";
  slantBefore?: "up" | "down" | "none";
  slantAfter?: "up" | "down" | "none";
  hiddenOnMobile?: boolean;
  children: React.ReactNode;
};

export const HomeSection = ({
  bg,
  slantCurrent = "none",
  slantBefore = "none",
  slantAfter = "none",
  hiddenOnMobile = false,
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
      className={`${bg} w-screen ${flex} ${slantBeforeFix} ${slantAfterFix} ${slant}`}
    >
      <section className="flex flex-col items-center max-w-6xl z-[2] py-8">
        {children}
      </section>
    </div>
  );
};
