import { UUID } from "crypto";

import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";

import { BrainUser } from "./components/BrainUser/BrainUser";
import { useBrainUsers } from "./hooks/useBrainUsers";

type BrainUsersProps = {
  brainId: UUID;
};
export const BrainUsers = ({ brainId }: BrainUsersProps): JSX.Element => {
  const { brainUsers, fetchBrainUsers } = useBrainUsers(brainId);

  if (brainUsers.length === 0) {
    return (
      <MessageInfoBox type="info">
        You are the only user to have access to this brain.
      </MessageInfoBox>
    );
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
