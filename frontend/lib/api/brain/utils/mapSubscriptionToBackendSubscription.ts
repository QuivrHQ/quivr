import { BrainRoleType } from "@/lib/components/BrainUsers/types";

import { Subscription } from "../brain";

export type BackendSubscription = { email: string; rights: BrainRoleType };

export const mapSubscriptionToBackendSubscription = (
  subscription: Subscription
): BackendSubscription => ({
  email: subscription.email,
  rights: subscription.role,
});
