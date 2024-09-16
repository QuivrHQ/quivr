"use client";

import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./AssistantTab.module.scss";

const AssistantTab = (): JSX.Element => {
  return (
    <div className={styles.assistant_tab_wrapper}>
      <div className={styles.form_wrapper}>Form</div>
      <div className={styles.button_wrapper}>
        <QuivrButton
          iconName="chevronRight"
          label="Executer"
          color="primary"
          important={true}
        />
      </div>
    </div>
  );
};

export default AssistantTab;
