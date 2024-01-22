import { Color } from "@/lib/types/Colors";
import { IconSize } from "@/lib/types/Icons";

import { Icon } from "../Icon/Icon";
// eslint-disable-next-line import/order
import styles from "./LoaderIcon.module.scss";

interface LoaderIconProps {
  size: IconSize;
  color: Color;
}

export const LoaderIcon = (props: LoaderIconProps): JSX.Element => {
  return (
    <Icon
      name="loader"
      size={props.size}
      color={props.color}
      classname={styles.loader_icon ?? ""}
    />
  );
};
