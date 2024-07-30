import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useUserData } from "@/lib/hooks/useUserData";

import styles from "./ProfileButton.module.scss";

export const ProfileButton = (): JSX.Element => {
  const [isHovered, setIsHovered] = useState<boolean>(false);
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/user");
  const { userIdentityData } = useUserData();
  const { getUserCredits } = useUserApi();
  const { remainingCredits, setRemainingCredits } = useUserSettingsContext();

  let username = userIdentityData?.username ?? "Profile";

  useEffect(() => {
    username = userIdentityData?.username ?? "Profile";
  }, [userIdentityData]);

  useEffect(() => {
    void (async () => {
      const res = await getUserCredits();
      setRemainingCredits(res);
    })();
  }, []);

  return (
    <Link
      className={styles.button_wrapper}
      href="/user"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <MenuButton
        label={username}
        iconName="user"
        type="open"
        isSelected={isSelected}
        color="primary"
        parentHovered={isHovered}
      />
      {remainingCredits !== null && (
        <div className={styles.credits}>
          <span className={styles.number}>{remainingCredits}</span>
          <Icon name="coin" color="gold" size="normal"></Icon>
        </div>
      )}
    </Link>
  );
};
