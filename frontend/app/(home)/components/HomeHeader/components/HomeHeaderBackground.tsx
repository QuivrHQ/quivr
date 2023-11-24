import styles from "../HomeHeader.module.css";

export const HomeHeaderBackground = (): JSX.Element => {
  return (
    <div className="relative overflow-visible h-0 z-[-1]">
      <div
        className={`bg-gradient-to-b from-sky-400 to-sky-900 ${
          styles["bg-slanted-upwards"] ?? ""
        } w-screen h-[22vh] sm:h-[40vh] md:h-[45vh] lg:h-[60vh] z-[-1]`}
      ></div>
    </div>
  );
};
