import { useEffect, useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./FoldableSection.module.scss";

import { Icon } from "../Icon/Icon";

interface FoldableSectionProps {
  label: string;
  icon: keyof typeof iconList;
  children: React.ReactNode;
  foldedByDefault?: boolean;
  hideBorderIfUnfolded?: boolean;
}

export const FoldableSection = (props: FoldableSectionProps): JSX.Element => {
  const [folded, setFolded] = useState<boolean>(false);

  useEffect(() => {
    setFolded(props.foldedByDefault ?? false);
  }, [props.foldedByDefault]);

  return (
    <div
      className={`
      ${styles.foldable_section_wrapper} 
      ${!folded ? styles.unfolded : ""}
      ${props.hideBorderIfUnfolded && folded ? styles.hide_border : ""}
      `}
    >
      <div className={styles.header_wrapper} onClick={() => setFolded(!folded)}>
        <div className={styles.header_left}>
          <Icon name={props.icon} size="normal" color="primary" />
          <p className={styles.header_title}>{props.label}</p>
        </div>
        <Icon
          name="chevronDown"
          size="normal"
          color="black"
          classname={`${styles.iconRotate} ${
            folded ? styles.iconRotateDown : styles.iconRotateUp
          }`}
        />
      </div>
      <div
        className={`${styles.contentWrapper} ${
          folded ? styles.contentCollapsed : styles.contentExpanded
        }`}
      >
        {props.children}
      </div>
    </div>
  );
};
