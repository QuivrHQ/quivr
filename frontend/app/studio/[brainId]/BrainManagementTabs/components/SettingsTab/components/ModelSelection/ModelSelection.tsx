import { UUID } from "crypto";
import { useTranslation } from "react-i18next";

import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";
import { Model } from "@/lib/types/BrainConfig";

import styles from "./ModelSelection.module.scss";

import { useBrainFormState } from "../../hooks/useBrainFormState";

type ModelSelectionProps = {
	brainId: UUID;
	handleSubmit: (checkDirty: boolean) => Promise<void>;
	hasEditRights: boolean;
	accessibleModels: string[];
};

export const ModelSelection = (props: ModelSelectionProps): JSX.Element => {
	const { t } = useTranslation(["translation", "brain"]);

	const { model, maxTokens, register, setModel } = useBrainFormState();
	const { handleSubmit, hasEditRights, accessibleModels } = props;

	const accessibleModelOptions = accessibleModels.map((accessibleModel) => {
		return { value: accessibleModel, label: accessibleModel };
	});

	return (
		<div className={styles.model_selection_wrapper}>
			<fieldset
				{...register("model", {
					value: accessibleModelOptions[0].value as Model,
				})}
			>
				<FieldHeader
					label={t("models", { ns: "translation" })}
					iconName="robot"
					help={t("model_description", { ns: "brain" })}
				/>
				<div className={styles.model}>
					<SingleSelector
						options={accessibleModelOptions}
						onChange={(option) => {
							setModel(option as Model);
							void handleSubmit(false);
						}}
						selectedOption={{ value: model, label: model }}
						placeholder={t("select_a_model", { ns: "translation" })}
						iconName="robot"
					/>
				</div>
			</fieldset>
			<fieldset>
				<FieldHeader
					label={t("max_tokens", { ns: "brain" })}
					iconName="hashtag"
					help={t("max_tokens_description", { ns: "brain" })}
				/>
				<div className={styles.max_tokens}>
					<input
						className={styles.slider}
						type="range"
						min="10"
						max={defineMaxTokens(model)}
						value={maxTokens || ""}
						disabled={!hasEditRights}
						{...register("maxTokens")}
					/>
					<span>{maxTokens}</span>
				</div>
			</fieldset>
		</div>
	);
};
