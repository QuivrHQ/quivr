import { StripePricingModal } from "@/lib/components/Stripe";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useUserData } from "@/lib/hooks/useUserData";

export const StripePricingOrManageButton = (): JSX.Element => {
  const { userData } = useUserData();

  const is_premium = userData?.is_premium ?? false;

  return (
    <StripePricingModal
      Trigger={
        <QuivrButton
          iconName="star"
          label={is_premium ? "Manage my plan" : "Upgrade my plan"}
          color="gold"
        ></QuivrButton>
      }
    />
  );
};
