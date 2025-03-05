"use client";

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { useUserData } from "@/lib/hooks/useUserData";
import { ButtonType } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import { Analytics } from "./BrainsTabs/components/Analytics/Analytics";
import { ManageBrains } from "./BrainsTabs/components/ManageBrains/ManageBrains";
import styles from "./page.module.scss";

const Studio = (): JSX.Element => {
	const { t } = useTranslation(["translation", "brain", "knowledge"]);

	const [selectedTab, setSelectedTab] = useState(t("manage_my_brains", { ns: "brain" }));
	const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();
	const { setIsBrainCreationModalOpened } = useBrainCreationContext();
	const { allBrains } = useBrainContext();
	const { userData } = useUserData();

	const studioTabs: Tab[] = [
		{
			label: t("manage_my_brains", { ns: "brain" }),
			isSelected: selectedTab === t("manage_my_brains", { ns: "brain" }),
			onClick: () => setSelectedTab(t("manage_my_brains", { ns: "brain" })),
			iconName: "edit",
		},
		{
			label: t("analytics", { ns: "brain" }),
			isSelected: selectedTab === t("analytics", { ns: "brain" }),
			onClick: () => setSelectedTab(t("analytics", { ns: "brain" })),
			iconName: "graph",
		},
	];

	const [buttons, setButtons] = useState<ButtonType[]>([
		{
			label: t("createBrain", { ns: "brain" }),
			color: "primary",
			onClick: () => {
				setIsBrainCreationModalOpened(true);
			},
			iconName: "brain",
			tooltip:
				t("tooltip_brain_maximum_number", { ns: "brain" }),
		},
		{
			label: t("addKnowledgeTitle", { ns: "knowledge" }),
			color: "primary",
			onClick: () => {
				setShouldDisplayFeedCard(true);
			},
			iconName: "uploadFile",
		},
	]);

	useEffect(() => {
		if (userData) {
			setButtons((prevButtons) => {
				return prevButtons.map((button) => {
					if (button.label === t("createBrain", { ns: "brain" })) {
						return {
							...button,
							disabled:
								userData.max_brains <=
								allBrains.filter((brain) => brain.brain_type === "doc").length,
						};
					}

					return button;
				});
			});
		}
	}, [userData?.max_brains, allBrains.length]);

	return (
		<div className={styles.page_wrapper}>
			<div className={styles.page_header}>
				<PageHeader
					iconName="brainCircuit"
					label={t("manage_brains", { ns: "brain" })}
					buttons={buttons}
				/>
			</div>
			<div className={styles.content_wrapper}>
				<Tabs tabList={studioTabs} />
				{selectedTab === t("manage_my_brains", { ns: "brain" }) && <ManageBrains />}
				{selectedTab === t("analytics", { ns: "brain" }) && <Analytics />}
			</div>
			<UploadDocumentModal />
			<AddBrainModal />
		</div>
	);
};

export default Studio;
