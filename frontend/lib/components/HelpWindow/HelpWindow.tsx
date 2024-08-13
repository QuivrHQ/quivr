import { useHelpContext } from "@/lib/context/HelpProvider/hooks/useHelpContext";

import styles from "./HelpWindow.module.scss";

export const HelpWindow = (): JSX.Element => {
  const { isVisible } = useHelpContext();

  if (!isVisible) {
    return <></>;
  }

  return <div className={styles.help_wrapper}>hey</div>;
};
