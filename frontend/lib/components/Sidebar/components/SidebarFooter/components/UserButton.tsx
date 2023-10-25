import { FaCrown } from "react-icons/fa";

import { Avatar } from "@/lib/components/ui/Avatar";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserData } from "@/lib/hooks/useUserData";

import { SidebarFooterButton } from "./SidebarFooterButton";
import { useGravatar } from "../../../../../hooks/useGravatar";

export const UserButton = (): JSX.Element => {
  const { session } = useSupabase();
  const { gravatarUrl } = useGravatar();
  const { userData } = useUserData();
  const is_premium = userData?.is_premium ?? false;
  const email = session?.user.email ?? "";
  const label = (
    <span className="flex justify-between items-center flex-nowrap gap-1 w-full">
      <span className="text-ellipsis overflow-hidden">{email}</span>
      {is_premium && <FaCrown className="w-5 h-5 shrink-0" />}
    </span>
  );

  return (
    <SidebarFooterButton
      href={"/user"}
      icon={<Avatar url={gravatarUrl} />}
      label={label}
    />
  );
};
