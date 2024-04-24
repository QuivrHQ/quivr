import { useEffect, useState } from "react";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { ButtonType } from "@/lib/types/QuivrButton";

import styles from "./PageHeader.module.scss";

import { Icon } from "../ui/Icon/Icon";
import { QuivrButton } from "../ui/QuivrButton/QuivrButton";

type Props = {
  iconName: string;
  label: string;
  buttons: ButtonType[];
};

export const PageHeader = ({
  iconName,
  label,
  buttons,
}: Props): JSX.Element => {
  const { isOpened } = useMenuContext();
  const { isDarkMode, setIsDarkMode } = useUserSettingsContext();
  const [lightModeIconName, setLightModeIconName] = useState("sun");
  const [remainingCredits, setRemainingCredits] = useState<number>(0);
  const { getUserCredits } = useUserApi();

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode);
  };

  useEffect(() => {
    setLightModeIconName(isDarkMode ? "sun" : "moon");

    void (async () => {
      const res = await getUserCredits();
      if (res) {
        setRemainingCredits(res);
      }
    });
  }, [isDarkMode]);

  return (
    <div className={styles.page_header_wrapper}>
      <div className={`${styles.left} ${!isOpened ? styles.menu_closed : ""}`}>
        <Icon name={iconName} size="large" color="primary" />
        <span>{label}</span>
      </div>
      <div className={styles.buttons_wrapper}>
        {buttons.map((button, index) => (
          <QuivrButton
            key={index}
            label={button.label}
            onClick={button.onClick}
            color={button.color}
            iconName={button.iconName}
            hidden={button.hidden}
          />
        ))}
        <Icon
          name={lightModeIconName}
          color="black"
          handleHover={true}
          size="small"
          onClick={toggleTheme}
        />
        {remainingCredits}
      </div>
    </div>
  );
};

export default PageHeader;
