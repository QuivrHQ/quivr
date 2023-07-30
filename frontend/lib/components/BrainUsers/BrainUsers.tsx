import { UUID } from "crypto";

import { BrainUser } from "./components";
import { useBrainUsers } from "./hooks/useBrainUsers";

type BrainUsersProps = {
  brainId: UUID;
};
export const BrainUsers = ({ brainId }: BrainUsersProps): JSX.Element => {
  const { brainUsers, fetchBrainUsers, isFetchingBrainUsers } =
    useBrainUsers(brainId);
  if (isFetchingBrainUsers) {
    return <p className="text-gray-500">Loading...</p>;
  }

  if (brainUsers.length === 0) {
    return <p className="text-gray-500">No user</p>;
  }

  return (
    <>
      {brainUsers.map((subscription) => (
        <BrainUser
          key={subscription.email}
          email={subscription.email}
          role={subscription.role}
          brainId={brainId}
          fetchBrainUsers={fetchBrainUsers}
        />
      ))}
    </>
  );
};
