import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { useUserData } from "@/lib/hooks/useUserData";

export const ProfileButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/user");
  const { userIdentityData } = useUserData();

  let username = userIdentityData?.username ?? "Profile";

  useEffect(() => {
    username = userIdentityData?.username ?? "Profile";
  }, [userIdentityData]);

  return (
    <Link href="/user">
      <MenuButton
        label={username}
        iconName="user"
        type="open"
        isSelected={isSelected}
        color="primary"
      />
    </Link>
  );
};
