import { UUID } from "crypto";

import { Subscription } from "@/lib/api/brain/brain";

import { BrainUser } from "./BrainUser";

type BrainUsersProps = {
  users: Subscription[];
  brainId: UUID;
  fetchBrainUsers: () => Promise<void>;
  isFetchingBrainUsers: boolean;
};
export const BrainUsers = ({
  users,
  brainId,
  fetchBrainUsers,
  isFetchingBrainUsers,
}: BrainUsersProps): JSX.Element => {
  if (isFetchingBrainUsers) {
    return <p className="text-gray-500">Loading...</p>;
  }

  if (users.length === 0) {
    return <p className="text-gray-500">No users</p>;
  }

  return (
    <>
      {users.map((subscription) => (
        <BrainUser
          key={subscription.email}
          email={subscription.email}
          rights={subscription.rights}
          brainId={brainId}
          fetchBrainUsers={fetchBrainUsers}
        />
      ))}
    </>
  );
};
