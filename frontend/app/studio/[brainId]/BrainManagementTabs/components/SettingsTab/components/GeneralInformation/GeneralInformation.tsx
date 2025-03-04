/* eslint max-lines:["error", 150] */
import { Controller } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./GeneralInformation.module.scss";

type GeneralInformationProps = {
	hasEditRights: boolean;
};

export const GeneralInformation = (
	props: GeneralInformationProps
): JSX.Element => {
	const { t } = useTranslation(["translation", "brain"]);

	const { hasEditRights } = props;

	return (
		<>
			<div className={styles.general_info_wrapper}>
				<div className={styles.name_field_wrapper}>
					<FieldHeader label={t("name", { ns: "translation" })} iconName="brain" />
					<Controller
						name="name"
						defaultValue=""
						render={({ field }) => (
							<TextInput
								label={t("name", { ns: "translation" })}
								inputValue={field.value as string}
								setInputValue={field.onChange}
								disabled={!hasEditRights}
							/>
						)}
					/>
				</div>

				<div className={styles.field_wrapper}>
					<FieldHeader label={t("description_title", { ns: "translation" })} iconName="paragraph" />
					<Controller
						name="description"
						defaultValue=""
						render={({ field }) => (
							<TextAreaInput
								label={t("description_title", { ns: "translation" })}
								inputValue={field.value as string}
								setInputValue={field.onChange}
								disabled={!hasEditRights}
							/>
						)}
					/>
				</div>
			</div>
		</>
	);
};
