"use client";

import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./page.module.scss";

const BrainsManagement = (): JSX.Element => {
  return (
    <div className={styles.page_wrapper}>
      <div className={styles.title_wrapper}>
        <Icon name="brainCircuit" size="big" color="primary" />
        <h1 className={styles.title}>Quivr Studio</h1>
      </div>
    </div>
  );
};

export default BrainsManagement;
