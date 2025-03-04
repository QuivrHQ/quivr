import { useState } from "react";
import { Controller, useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types/types";
import { BrainSnippet } from "@/lib/components/BrainSnippet/BrainSnippet";
import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./BrainMainInfosStep.module.scss";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationSteps } from "../../hooks/useBrainCreationSteps";

export const BrainMainInfosStep = (): JSX.Element => {
	const { t } = useTranslation(["brain", "translation"]);

	const [editSnippet, setEditSnippet] = useState<boolean>(false);
	const { currentStepIndex, goToNextStep } = useBrainCreationSteps();
	const { snippetColor, setSnippetColor, snippetEmoji, setSnippetEmoji } =
		useBrainCreationContext();

	const { watch } = useFormContext<CreateBrainProps>();
	const name = watch("name");
	const description = watch("description");

	const isDisabled = !name || !description;

	const next = (): void => {
		goToNextStep();
	};

	if (currentStepIndex !== 0) {
		return <></>;
	}

	return (
		<div className={styles.brain_main_infos_container}>
			<div className={styles.brain_main_infos_wrapper}>
				<div className={styles.inputs_wrapper}>
					<span className={styles.title}>{t("defind_brain_identity", { ns: "brain" })}</span>
					<div className={styles.first_line_wrapper}>
						<div className={styles.name_field}>
							<FieldHeader iconName="brain" label={t("name", { ns: "translation" })} mandatory={true} />
							<Controller
								name="name"
								render={({ field }) => (
									<TextInput
										label={t("enter_brain_name", { ns: "brain" })}
										inputValue={field.value as string}
										setInputValue={field.onChange}
									/>
								)}
							/>
						</div>
						<div className={styles.brain_snippet_wrapper}>
							<div
								className={styles.brain_snippet}
								style={{ backgroundColor: snippetColor }}
								onClick={() => {
									if (!editSnippet) {
										setEditSnippet(true);
									}
								}}
							>
								<span>{snippetEmoji}</span>
							</div>
							<QuivrButton
								label={t("editButton", { ns: "brain" })}
								iconName="edit"
								color="primary"
								onClick={() => setEditSnippet(true)}
								small={true}
							/>
						</div>
					</div>
					<div>
						<FieldHeader
							iconName="paragraph"
							label={t("description_title", { ns: "translation" })}
							mandatory={true}
						/>
						<Controller
							name="description"
							render={({ field }) => (
								<TextAreaInput
									label={t("enter_brain_description", { ns: "brain" })}
									inputValue={field.value as string}
									setInputValue={field.onChange}
								/>
							)}
						/>
					</div>
				</div>
				<div className={styles.buttons_wrapper}>
					<QuivrButton
						color="primary"
						label={t("next", { ns: "translation" })}
						onClick={() => next()}
						iconName="chevronRight"
						disabled={isDisabled}
						important={true}
					/>
				</div>
			</div>
			{editSnippet && (
				<div className={styles.edit_snippet}>
					<BrainSnippet
						setVisible={setEditSnippet}
						initialColor={snippetColor}
						initialEmoji={snippetEmoji}
						onSave={(color: string, emoji: string) => {
							setSnippetColor(color);
							setSnippetEmoji(emoji);
						}}
					/>
				</div>
			)}
		</div>
	);
};
