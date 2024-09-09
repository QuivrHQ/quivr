import { useEffect, useState } from "react";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./SocialsButtons.module.scss";

export const SocialsButtons = (): JSX.Element => {
  const { isDarkMode, setIsDarkMode } = useUserSettingsContext();
  const [lightModeIconName, setLightModeIconName] = useState("sun");

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  useEffect(() => {
    setLightModeIconName(isDarkMode ? "sun" : "moon");
  }, [isDarkMode]);

  const handleClick = (url: string) => {
    window.open(url, "_blank");
  };

  return (
    <div className={styles.socials_buttons_wrapper}>
      <div className={styles.left}>
        <Icon
          name="github"
          color="black"
          size="small"
          handleHover={true}
          onClick={() => handleClick("https://github.com/QuivrHQ/quivr")}
        />
        <Icon
          name="linkedin"
          color="black"
          size="small"
          handleHover={true}
          onClick={() =>
            handleClick("https://www.linkedin.com/company/getquivr")
          }
        />
        <Icon
          name="twitter"
          color="black"
          size="small"
          handleHover={true}
          onClick={() => handleClick("https://twitter.com/quivr_brain")}
        />
        <Icon
          name="discord"
          color="black"
          size="small"
          handleHover={true}
          onClick={() => handleClick("https://discord.gg/HUpRgp2HG8")}
        />
      </div>
      <Icon
        name={lightModeIconName}
        color="black"
        handleHover={true}
        size="normal"
        onClick={toggleTheme}
      />
    </div>
  );
};
