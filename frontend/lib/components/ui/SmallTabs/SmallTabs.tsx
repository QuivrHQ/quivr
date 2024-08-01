import { Tab } from "@/lib/types/Tab";

import styles from "./SmallTabs.module.scss";

type TabsProps = {
  tabList: Tab[];
};

export const SmallTabs = ({ tabList }: TabsProps): JSX.Element => {
  return <div className={styles.tabs_container}>{tabList.length}</div>;
};
