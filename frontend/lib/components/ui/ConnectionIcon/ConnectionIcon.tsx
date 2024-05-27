import styles from "./ConnectionIcon.module.scss";

interface ConnectionIconProps {
  letter: string;
  index: number;
}

export const ConnectionIcon = ({
  letter,
  index,
}: ConnectionIconProps): JSX.Element => {
  const colors = ["#FBBC04", "#F28B82", "#8AB4F8", "#81C995", "#C58AF9"];

  return (
    <div
      className={styles.connection_icon}
      style={{ backgroundColor: colors[index % 5] }}
    >
      {letter.toUpperCase()}
    </div>
  );
};
