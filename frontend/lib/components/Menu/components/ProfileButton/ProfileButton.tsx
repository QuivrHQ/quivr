import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const ProfileButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/user");

  return (
    <Link href="/user">
      <MenuButton
        label="Profile"
        iconName="user"
        type="open"
        isSelected={isSelected}
        color="primary"
      />
    </Link>
  );
};
