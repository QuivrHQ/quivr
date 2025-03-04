import { Controller } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";

import styles from "./Prompt.module.scss";

export const Prompt = (): JSX.Element => {
	const { t } = useTranslation(["brain"]);

	return (
		<div className={styles.prompt_wrapper}>
			<div>
				<FieldHeader label={t("instructions", { ns: "brain" })} iconName="paragraph" />
				<Controller
					name="prompt.content"
					defaultValue=""
					render={({ field }) => (
						<TextAreaInput
							label={t("instructions_placeholder", { ns: "brain" })}
							inputValue={field.value as string}
							setInputValue={field.onChange}
						/>
					)}
				/>
			</div>
		</div>
	);
};
