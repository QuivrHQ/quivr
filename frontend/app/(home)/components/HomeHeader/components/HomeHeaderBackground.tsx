import styles from "../HomeHeader.module.css";

export const HomeHeaderBackground = (): JSX.Element => {
  return (
    <div className="relative overflow-visible h-0 z-[-1]">
      <div
        className={`bg-gradient-to-b from-[#7A27FD] to-[#D07DF9] ${
          styles["bg-slanted-upwards"] ?? ""
        } w-screen h-[30vh] lg:h-[50vh] z-[-1]`}
      ></div>
    </div>
  );
};
