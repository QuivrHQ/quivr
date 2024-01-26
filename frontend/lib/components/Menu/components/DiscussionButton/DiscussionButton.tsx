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
        <span>New thread</span>
        <Icon
          name="search"
          size="normal"
          color={hovered ? "accent" : "black"}
        />
      </div>
    </Link>
  );
};
