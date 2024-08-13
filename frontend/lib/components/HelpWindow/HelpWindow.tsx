import { useEffect, useRef } from "react";

import { useHelpContext } from "@/lib/context/HelpProvider/hooks/useHelpContext";

import styles from "./HelpWindow.module.scss";

import { Icon } from "../ui/Icon/Icon";

export const HelpWindow = (): JSX.Element => {
  const { isVisible, setIsVisible } = useHelpContext();
  const helpWindowRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        helpWindowRef.current &&
        !helpWindowRef.current.contains(event.target as Node)
      ) {
        setIsVisible(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [setIsVisible]);

  if (!isVisible) {
    return <></>;
  }

  return (
    <div className={styles.help_wrapper} ref={helpWindowRef}>
      <div className={styles.header}>
        <span className={styles.title}>🧠 What is Quivr ?</span>
        <Icon
          name="close"
          size="normal"
          color="black"
          handleHover={true}
          onClick={() => setIsVisible(false)}
        />
      </div>
    </div>
  );
};
