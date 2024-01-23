"use client";

import styles from "./DataPanel.module.scss";
import RelatedBrains from "./components/RelatedBrains/RelatedBrains";

const DataPanel = (): JSX.Element => {
  return (
    <div className={styles.data_panel_wrapper}>
      <RelatedBrains />
    </div>
  );
};

export default DataPanel;
