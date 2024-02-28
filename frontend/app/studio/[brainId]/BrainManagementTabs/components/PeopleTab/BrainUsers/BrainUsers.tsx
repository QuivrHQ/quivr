import { UUID } from "crypto";
import { useTranslation } from "react-i18next";

import { BrainUser } from "./components";
import { useBrainUsers } from "./hooks/useBrainUsers";

import { MessageInfoBox } from "../../../../../../../lib/components/ui/MessageInfoBox/MessageInfoBox";

type BrainUsersProps = {
  brainId: UUID;
};
export const BrainUsers = ({ brainId }: BrainUsersProps): JSX.Element => {
  const { t } = useTranslation(["translation", "config"]);
  const { brainUsers, fetchBrainUsers, isFetchingBrainUsers } =
    useBrainUsers(brainId);
  if (isFetchingBrainUsers) {
    return <p className="text-gray-500">{t("loading")}</p>;
  }

  if (brainUsers.length === 0) {
    return (
      <MessageInfoBox
        type="info"
        content="You the only user to have access to this brain."
      />
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
