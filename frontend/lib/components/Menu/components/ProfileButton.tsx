import Link from "next/link";
import { LuChevronRight, LuUser } from "react-icons/lu";

import { Button } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ActionsModal/components/Button";

export const ProfileButton = (): JSX.Element => {
  return (
    <Link href="/user">
      <Button
        label="Profile"
        startIcon={
          <div className="p-3 bg-secondary text-primary rounded-full">
            <LuUser size={25} />
          </div>
        }
        endIcon={<LuChevronRight size={18} />}
        className="font-extrabold w-full hover:bg-secondary p-0"
      />
    </Link>
  );
};
