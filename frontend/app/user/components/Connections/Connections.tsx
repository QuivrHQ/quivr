import { useTranslation } from "react-i18next";

import { ConnectionCards } from "@/lib/components/ConnectionCards/ConnectionCards";

import styles from "./Connections.module.scss";

export const Connections = (): JSX.Element => {
	const { t } = useTranslation(["translation"]);

	return (
		<div className={styles.connections_wrapper}>
			<span className={styles.title}>{t("link_apps_to_your_account", { ns: "translation" })}</span>
			<ConnectionCards />
		</div>
	);
};
