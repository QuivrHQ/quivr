import Link from "next/link";
import { FaBrain } from "react-icons/fa";

import { sidebarLinkStyle } from "@/app/chat/components/ChatsList/components/ChatsListItem/styles/SidebarLinkStyle";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const BrainManagementButton = (): JSX.Element => {
  const { currentBrainId } = useBrainContext();

  return (
    <Link
      href={`/brains-management/${currentBrainId ?? ""}`}
      className={sidebarLinkStyle}
    >
      <FaBrain className="w-8 h-8" />
      <span>My Brains</span>
    </Link>
  );
};
