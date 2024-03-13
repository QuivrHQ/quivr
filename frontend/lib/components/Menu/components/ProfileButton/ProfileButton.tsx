import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { useUserData } from "@/lib/hooks/useUserData";

export const ProfileButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/user");
  const { userIdentityData } = useUserData();

  return (
    <Link href="/user">
      <MenuButton
        label={userIdentityData?.username ?? "Profile"}
        iconName="user"
        type="open"
        isSelected={isSelected}
        color="primary"
      />
    </Link>
  );
};
