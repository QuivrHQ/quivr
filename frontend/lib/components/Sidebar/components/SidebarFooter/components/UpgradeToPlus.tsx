import { useFeatureIsOn } from "@growthbook/growthbook-react";
import { FiUser } from "react-icons/fi";

import { Modal } from "@/lib/components/ui/Modal";
import { useUserData } from "@/lib/hooks/useUserData";

import { sidebarLinkStyle } from "../styles/SidebarLinkStyle";

const PRICING_TABLE_ID = process.env.NEXT_PUBLIC_STRIPE_PRICING_TABLE_ID;
const PUBLISHABLE_KEY = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;

export const UpgradeToPlus = (): JSX.Element => {
  const { userData } = useUserData();
  const is_premium = userData?.is_premium;
  const featureIsOn = useFeatureIsOn("monetization");

  if (!featureIsOn || is_premium === true) {
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
      <script async src="https://js.stripe.com/v3/pricing-table.js"></script>
      <stripe-pricing-table
        pricing-table-id={PRICING_TABLE_ID}
        publishable-key={PUBLISHABLE_KEY}
      ></stripe-pricing-table>
    </Modal>
  );
};
