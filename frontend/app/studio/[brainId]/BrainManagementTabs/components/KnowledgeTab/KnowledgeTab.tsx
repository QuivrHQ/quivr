"use client";
import { UUID } from "crypto";
import { AnimatePresence, motion } from "framer-motion";
import { useTranslation } from "react-i18next";

import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";
import { Knowledge } from "@/lib/types/Knowledge";

import styles from "./KnowledgeTab.module.scss";
import KnowledgeTable from "./KnowledgeTable/KnowledgeTable";
import { useAddedKnowledge } from "./hooks/useAddedKnowledge";

type KnowledgeTabProps = {
	brainId: UUID;
	hasEditRights: boolean;
	allKnowledge: Knowledge[];
};
export const KnowledgeTab = ({
	brainId,
	allKnowledge,
	hasEditRights,
}: KnowledgeTabProps): JSX.Element => {
	const { t } = useTranslation(["knowledge", "brain"]);

	const { isPending } = useAddedKnowledge({
		brainId,
	});
	const { setShouldDisplayFeedCard } = useKnowledgeToFeedContext();

	if (!hasEditRights) {
		return (
			<div className={styles.knowledge_tab_container}>
				<div className={styles.knowledge_tab_wrapper}>
					<MessageInfoBox type="warning">
						{t("dont_have_permission", { ns: "brain" })}
					</MessageInfoBox>
				</div>
			</div>
		);
	}

	if (isPending) {
		return <LoaderIcon size="big" color="accent" />;
	}

	if (allKnowledge.length === 0) {
		return (
			<div className={styles.knowledge_tab_container}>
				<div className={styles.knowledge_tab_wrapper}>
					<MessageInfoBox type="warning">
						<div className={styles.message}>
							{t("brain_empty", { ns: "brain" })}
							<QuivrButton
								label={t("addKnowledgeTitle", { ns: "knowledge" })}
								color="primary"
								iconName="add"
								onClick={() => setShouldDisplayFeedCard(true)}
							/>
							.
						</div>
					</MessageInfoBox>
				</div>
			</div>
		);
	}

	return (
		<div className={styles.knowledge_tab_container}>
			<div className={styles.knowledge_tab_wrapper}>
				<motion.div layout className="w-full flex flex-col gap-5">
					<AnimatePresence mode="popLayout">
						<KnowledgeTable knowledgeList={allKnowledge} />
					</AnimatePresence>
				</motion.div>
			</div>
		</div>
	);
};
