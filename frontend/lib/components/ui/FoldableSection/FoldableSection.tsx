import { useEffect, useRef, useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./FoldableSection.module.scss";

import { Icon } from "../Icon/Icon";

interface FoldableSectionProps {
  label: string;
  icon: keyof typeof iconList;
  children: React.ReactNode;
  foldedByDefault?: boolean;
  hideBorder?: boolean;
}

export const FoldableSection = (props: FoldableSectionProps): JSX.Element => {
  const [folded, setFolded] = useState<boolean>(false);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setFolded(props.foldedByDefault ?? false);
  }, [props.foldedByDefault]);

  const getContentHeight = (): string => {
    return folded ? "0" : `${contentRef.current?.scrollHeight}px`;
  };

  return (
    <div
      className={`
      ${styles.foldable_section_wrapper} 
      ${!folded ? styles.unfolded : ""}
      ${props.hideBorder ? styles.hide_border : ""}
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
            folded ? styles.iconRotateDown : styles.iconRotateRight
          }`}
        />
      </div>
      <div
        ref={contentRef}
        className={`${styles.contentWrapper} ${
          folded ? styles.contentCollapsed : styles.contentExpanded
        }`}
        style={{ maxHeight: getContentHeight() }}
      >
        {props.children}
      </div>
    </div>
  );
};
