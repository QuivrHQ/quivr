"use client";

import { UUID } from "crypto";
import { useTranslation } from "react-i18next";

import { BrainUsers } from "@/app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/BrainUsers";
import { UserToInvite } from "@/app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/components/UserToInvite/UserToInvite";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useShareBrain } from "@/lib/hooks/useShareBrain";

import styles from "./PeopleTab.module.scss";

type ShareBrainModalProps = {
	brainId: UUID;
};

export const PeopleTab = ({ brainId }: ShareBrainModalProps): JSX.Element => {
	const { t } = useTranslation(["brain"]);

	const {
		roleAssignations,
		updateRoleAssignation,
		removeRoleAssignation,
		inviteUsers,
		addNewRoleAssignationRole,
		sendingInvitation,
		canAddNewRow,
	} = useShareBrain(brainId);

	return (
		<div className={styles.people_tab_wrapper}>
			<form
				onSubmit={(event) => {
					event.preventDefault();
					void inviteUsers();
				}}
			>
				<div className={styles.section_wrapper}>
					<span className={styles.section_title}>{t("invite_new_users", { ns: "brain" })}</span>
					{roleAssignations.map((roleAssignation, index) => (
						<UserToInvite
							key={roleAssignation.id}
							onChange={updateRoleAssignation(index)}
							removeCurrentInvitation={removeRoleAssignation(index)}
							roleAssignation={roleAssignation}
						/>
					))}
					<div className={styles.buttons_wrapper}>
						<QuivrButton
							onClick={addNewRoleAssignationRole}
							disabled={sendingInvitation || !canAddNewRow}
							label={t("add_new_user", { ns: "brain" })}
							color="primary"
							iconName="add"
						></QuivrButton>
						<QuivrButton
							isLoading={sendingInvitation}
							disabled={
								!roleAssignations.some(
									(roleAssignation) => roleAssignation.email !== ""
								)
							}
							label={t("send_invitation", { ns: "brain" })}
							color="primary"
							iconName="invite"
							onClick={inviteUsers}
						></QuivrButton>
					</div>
				</div>
			</form>
			<div className={`${styles.section_wrapper} ${styles.last}`}>
				<span className={styles.section_title}>{t("user_with_access", { ns: "brain" })}</span>
				<BrainUsers brainId={brainId} />
			</div>
		</div>
	);
};
