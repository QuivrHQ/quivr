/* eslint-disable max-lines */

import { useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { Tab } from "@/lib/types/Tab";

import styles from "./BrainManagementTabs.module.scss";
import { KnowledgeTab } from "./components/KnowledgeTab/KnowledgeTab";
import { useAddedKnowledge } from "./components/KnowledgeTab/hooks/useAddedKnowledge";
import { PeopleTab } from "./components/PeopleTab/PeopleTab";
import { SettingsTab } from "./components/SettingsTab/SettingsTab";
import { useBrainFetcher } from "./hooks/useBrainFetcher";
import { useBrainManagementTabs } from "./hooks/useBrainManagementTabs";

export const BrainManagementTabs = (): JSX.Element => {
	const { t } = useTranslation(["translation", "brain"]);

	const [selectedTab, setSelectedTab] = useState("Knowledge");
	const { brainId, hasEditRights } = useBrainManagementTabs();
	const { allKnowledge } = useAddedKnowledge({ brainId: brainId ?? undefined });
	const router = useRouter();

	const { isLoading } = useBrainFetcher({
		brainId,
	});

	const brainManagementTabs: Tab[] = [
		{
			label: hasEditRights
				? `${t("knowledge", { ns: "brain" })} (${allKnowledge.length
				})`
				: t("knowledge", { ns: "brain" }),
			isSelected: selectedTab === "Knowledge",
			onClick: () => setSelectedTab("Knowledge"),
			iconName: "file",
		},
		{
			label: t("settings", { ns: "brain" }),
			isSelected: selectedTab === "Settings",
			onClick: () => setSelectedTab("Settings"),
			iconName: "settings",
		},
		{
			label: t("people", { ns: "brain" }),
			isSelected: selectedTab === "People",
			onClick: () => setSelectedTab("People"),
			iconName: "user",
			disabled: !hasEditRights,
		},
	];

	if (!brainId) {
		return <div />;
	}

	if (isLoading) {
		return (
			<div className={styles.loader}>
				<LoaderIcon size="big" color="primary" />
			</div>
		);
	}

	return (
		<div>
			<div className={styles.header_wrapper}>
				<Icon
					name="chevronLeft"
					size="normal"
					color="black"
					handleHover={true}
					onClick={() => router.push("/studio")}
				/>
				<div className={styles.tabs}>
					<Tabs tabList={brainManagementTabs} />
				</div>
			</div>
			{selectedTab === "Settings" && (
				<SettingsTab brainId={brainId} hasEditRights={hasEditRights} />
			)}
			{selectedTab === "People" && <PeopleTab brainId={brainId} />}
			{selectedTab === "Knowledge" && (
				<KnowledgeTab
					brainId={brainId}
					hasEditRights={hasEditRights}
					allKnowledge={allKnowledge}
				/>
			)}
		</div>
	);
};
