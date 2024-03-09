import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./SocialsButtons.module.scss";

export const SocialsButtons = (): JSX.Element => {
  return (
    <div className={styles.socials_buttons_wrapper}>
      <Icon name="github" color="black" size="small" handleHover={true}></Icon>
      <Icon
        name="linkedin"
        color="black"
        size="small"
        handleHover={true}
      ></Icon>
      <Icon name="twitter" color="black" size="small" handleHover={true}></Icon>
    </div>
  );
};
