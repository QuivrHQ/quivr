import { Avatar } from "@/lib/components/ui/Avatar";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import { SidebarFooterButton } from "./SidebarFooterButton";
import { useGravatar } from "../../../../../hooks/useGravatar";

export const UserButton = (): JSX.Element => {
  const { session } = useSupabase();
  const { gravatarUrl } = useGravatar();

  return (
    <SidebarFooterButton
      href={"/user"}
      icon={<Avatar url={gravatarUrl} />}
      label={session?.user.email ?? ""}
    />
  );
};
