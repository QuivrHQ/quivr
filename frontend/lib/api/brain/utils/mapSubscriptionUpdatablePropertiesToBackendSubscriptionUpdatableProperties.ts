import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";

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
