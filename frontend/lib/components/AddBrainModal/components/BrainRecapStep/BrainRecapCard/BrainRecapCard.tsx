import styles from "./BrainRecapCard.module.scss";

interface BrainRecapCardProps {
  label: string;
  number: number;
}

export const BrainRecapCard = ({
  label,
  number,
}: BrainRecapCardProps): JSX.Element => {
  return (
    <div className={styles.brain_recap_card_wrapper}>
      <span className={styles.number_label}>{number.toString()}</span>
      <span className={styles.type}>
        {label}
        {number > 1 ? "s" : ""}
      </span>
    </div>
  );
};
