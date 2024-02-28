import { BrainRoleType } from "@/app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/types";

import { Subscription } from "../brain";

export type BackendSubscription = { email: string; rights: BrainRoleType };

export const mapSubscriptionToBackendSubscription = (
  subscription: Subscription
): BackendSubscription => ({
  email: subscription.email,
  rights: subscription.role,
});
