import { Tab } from "@/lib/types/Tab";

import styles from "./Tabs.module.scss";

type TabsProps = {
  tabs: Tab[];
};

export const Tabs = ({ tabs }: TabsProps): JSX.Element => {
  return (
    <div className={styles.tabs_container}>
      {tabs.map((tab, index) => (
        <div key={index}>{tab.label}</div>
      ))}
    </div>
  );
};
