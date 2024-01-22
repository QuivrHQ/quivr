import Link from "next/link";
import { LuChevronRight, LuUser } from "react-icons/lu";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton";

export const ProfileButton = (): JSX.Element => {
  return (
    <Link href="/user">
      <MenuButton
        label="Profile"
        startIcon={
          <div className="p-3 bg-secondary text-primary rounded-full">
            <LuUser size={25} />
          </div>
        }
        endIcon={<LuChevronRight size={18} />}
        className="w-full hover:bg-secondary p-0"
      />
    </Link>
  );
};
