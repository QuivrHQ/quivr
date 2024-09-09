import { Tab } from "@/lib/types/Tab";

import styles from "./SmallTabs.module.scss";

type TabsProps = {
  tabList: Tab[];
};

export const SmallTabs = ({ tabList }: TabsProps): JSX.Element => {
  return (
    <div className={styles.tabs_container}>
      {tabList.map((tab, index) => (
        <div
          className={`
          ${styles.tab_wrapper}
          ${tab.isSelected ? styles.selected : ""}
          ${tab.disabled ? styles.disabled : ""}
          `}
          key={index}
          onClick={tab.onClick}
        >
          <div className={styles.label_wrapper}>
            <span className={styles.label}>{tab.label}</span>
            {!!tab.badge && tab.badge > 0 && (
              <div className={styles.label_badge}>{tab.badge}</div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};
