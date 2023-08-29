import { BrainRoleType } from "@/lib/components/BrainUsers/types";

import { SubscriptionUpdatableProperties } from "../types";

type BackendSubscriptionUpdatableProperties = {
  rights: BrainRoleType | null;
};
export const mapSubscriptionUpdatablePropertiesToBackendSubscriptionUpdatableProperties =
  (
    subscriptionUpdatableProperties: SubscriptionUpdatableProperties
  ): BackendSubscriptionUpdatableProperties => ({
    rights: subscriptionUpdatableProperties.role,
  });
