import { StripePricingModal } from "@/lib/components/Stripe";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useUserData } from "@/lib/hooks/useUserData";

const MANAGE_PLAN_URL = process.env.NEXT_PUBLIC_STRIPE_MANAGE_PLAN_URL;

type StripePricingModalButtonProps = {
  small?: boolean;
};

export const StripePricingOrManageButton = ({
  small = false,
}: StripePricingModalButtonProps): JSX.Element => {
  const { userData } = useUserData();

  const is_premium = userData?.is_premium ?? false;
  if (is_premium) {
    return (
      <a href={MANAGE_PLAN_URL} target="_blank" rel="noopener">
        <QuivrButton
          label="Manage my plan"
          color="gold"
          iconName="star"
          small={small}
        ></QuivrButton>
      </a>
    );
  }

  return (
    <StripePricingModal
      Trigger={
        <div>
          <QuivrButton
            label="Upgrade my plan"
            color="gold"
            iconName="star"
            small={small}
          ></QuivrButton>
        </div>
      }
      user_email={userData?.email ?? ""}
    />
  );
};
