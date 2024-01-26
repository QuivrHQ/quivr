import Link from "next/link";
import { useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./DiscussionButton.module.scss";

export const DiscussionButton = (): JSX.Element => {
  const [hovered, setHovered] = useState(false);

  return (
    <Link href="/search">
      <div
        className={styles.button_wrapper}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        <div className={styles.left_wrapper}>
          <span>New Search</span>
          <div className={styles.shortcuts_wrapper}>
            <div className={styles.shortcut}>⌘</div>
            <div className={styles.shortcut}>K</div>
          </div>
        </div>
        <Icon
          name="search"
          size="normal"
          color={hovered ? "accent" : "black"}
        />
      </div>
    </Link>
  );
};
