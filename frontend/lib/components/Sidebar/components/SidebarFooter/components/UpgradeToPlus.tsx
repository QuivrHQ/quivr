import { FiUser } from "react-icons/fi";

import { Modal } from "@/lib/components/ui/Modal";
import { useUserData } from "@/lib/hooks/useUserData";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

export const UpgradeToPlus = (): JSX.Element => {
  const { userData } = useUserData();
  const is_premium = userData?.is_premium;

  if (is_premium === true) {
    return <></>;
  }

  return (
    <Modal
      Trigger={
        <button type="button" className={sidebarLinkStyle}>
          <FiUser className="w-8 h-8" />
          <span>
            Upgrade to plus{" "}
            <span className="rounded bg-primary/50 py-1 px-3 text-xs">New</span>
          </span>
        </button>
      }
      CloseTrigger={<div />}
    >
      🚀
    </Modal>
  );
};
