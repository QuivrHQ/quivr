import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./InfoSection.module.scss";

interface InfoSectionProps {
  iconName: string;
  title: string;
  children: React.ReactNode;
  last?: boolean;
}

export const InfoSection = ({
  iconName,
  title,
  children,
  last,
}: InfoSectionProps): JSX.Element => (
  <div
    className={`${styles.info_wrapper} ${last ? styles.without_border : ""}`}
  >
    <div className={styles.title_wrapper}>
      <Icon name={iconName} color="grey" size="small" />
      <span className={styles.title}>{title}</span>
    </div>
    {children}
  </div>
);
