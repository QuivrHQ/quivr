import { useEffect, useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./FoldableSection.module.scss";

import { Icon } from "../Icon/Icon";

interface FoldableSectionProps {
  label: string;
  icon: keyof typeof iconList;
  children: React.ReactNode;
  foldedByDefault?: boolean;
}

export const FoldableSection = (props: FoldableSectionProps): JSX.Element => {
  const [folded, setFolded] = useState<boolean>(false);

  useEffect(() => {
    setFolded(props.foldedByDefault ?? false);
  }, [props.foldedByDefault]);

  return (
    <div className={styles.foldable_section_wrapper}>
      <div className={styles.header_wrapper} onClick={() => setFolded(!folded)}>
        <div className={styles.header_left}>
          <Icon name={props.icon} size="normal" color="black" />
          <p className={styles.header_title}>{props.label}</p>
        </div>
        <Icon
          name={folded ? "chevronDown" : "chevronRight"}
          size="large"
          color="accent"
        />
      </div>
      {!folded && <div>{props.children}</div>}
    </div>
  );
};
