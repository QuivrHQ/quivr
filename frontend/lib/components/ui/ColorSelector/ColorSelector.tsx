import { HexColorPicker } from "react-colorful";

import styles from "./ColorSelector.module.scss";

export const ColorSelector = ({
  onSelectColor,
  color,
}: {
  onSelectColor?: (emoji: string) => void;
  color: string;
}): JSX.Element => {
  return (
    <div className={styles.color_picker_wrapper}>
      <HexColorPicker color={color} onChange={onSelectColor} />
    </div>
  );
};
