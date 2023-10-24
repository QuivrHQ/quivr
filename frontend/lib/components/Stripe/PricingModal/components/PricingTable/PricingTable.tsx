const PRICING_TABLE_ID = process.env.NEXT_PUBLIC_STRIPE_PRICING_TABLE_ID;
const PUBLISHABLE_KEY = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY;

export const StripePricingTable = (): JSX.Element => {
  return (
    <>
      <script async src="https://js.stripe.com/v3/pricing-table.js"></script>
      <stripe-pricing-table
        pricing-table-id={PRICING_TABLE_ID}
        publishable-key={PUBLISHABLE_KEY}
      ></stripe-pricing-table>
    </>
  );
};
