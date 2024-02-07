import { Tab } from "@/lib/types/Tab";

import styles from "./Tabs.module.scss";

import { Icon } from "../Icon/Icon";

type TabsProps = {
  tabList: Tab[];
};

export const Tabs = ({ tabList }: TabsProps): JSX.Element => {
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
          <Icon
            name={tab.iconName}
            size="normal"
            color={tab.isSelected ? "primary" : tab.disabled ? "grey" : "black"}
          />
          <span className={styles.label}>{tab.label}</span>
        </div>
      ))}
    </div>
  );
};
