import { UUID } from "crypto";
import { useTranslation } from "react-i18next";

import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";

import { BrainUser } from "./components/BrainUser/BrainUser";
import { useBrainUsers } from "./hooks/useBrainUsers";

type BrainUsersProps = {
	brainId: UUID;
};
export const BrainUsers = ({ brainId }: BrainUsersProps): JSX.Element => {
	const { t } = useTranslation(["brain"]);

	const { brainUsers, fetchBrainUsers } = useBrainUsers(brainId);

	if (brainUsers.length === 0) {
		return (
			<MessageInfoBox type="info">
				{t("you_are_only_user_to_have_access_to_this_brain", { ns: "brain" })}
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
