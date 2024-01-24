import { useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./FoldableSection.module.scss";

import { Icon } from "../Icon/Icon";

interface FoldableSectionProps {
  label: string;
  icon: keyof typeof iconList;
  children: React.ReactNode;
}

export const FoldableSection = (props: FoldableSectionProps): JSX.Element => {
  const [folded, setFolded] = useState<boolean>(false);

  return (
    <div className={styles.foldable_section_wrapper}>
      <div className={styles.header_wrapper} onClick={() => setFolded(!folded)}>
        <div className={styles.header_left}>
          <Icon name={props.icon} size="normal" color="primary" />
          <span>{props.label}</span>
        </div>
        <Icon
          name={folded ? "chevronDown" : "chevronRight"}
          size="large"
          color="black"
        />
      </div>
      {!folded && <div>{props.children}</div>}
    </div>
  );
};
