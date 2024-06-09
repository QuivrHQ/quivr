import { useState } from "react";

import { Tab } from "@/lib/types/Tab";

import styles from "./Tabs.module.scss";

import { Icon } from "../Icon/Icon";

type TabsProps = {
  tabList: Tab[];
};

export const Tabs = ({ tabList }: TabsProps): JSX.Element => {
  const [tabHoveredIndex, setTabHoveredIndex] = useState<number | null>(null);

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
          onMouseEnter={() => setTabHoveredIndex(index)}
          onMouseLeave={() => setTabHoveredIndex(null)}
        >
          <Icon
            name={tab.iconName}
            size="normal"
            color={
              tab.isSelected || index === tabHoveredIndex
                ? "primary"
                : tab.disabled
                ? "grey"
                : "black"
            }
          />
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
