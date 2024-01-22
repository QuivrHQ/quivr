import { AiOutlineLoading3Quarters } from "react-icons/ai";

import { IconSize } from "@/lib/types/Icons";

import styles from "./LoaderIcon.module.scss";

interface LoaderIconProps {
  size: IconSize;
}

export const LoaderIcon = (props: LoaderIconProps): JSX.Element => {
  return (
    <AiOutlineLoading3Quarters
      className={`${styles.loader_icon ?? ""} ${styles[props.size] ?? ""}`}
    />
  );
};
