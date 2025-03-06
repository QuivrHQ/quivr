import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { useHelpContext } from "@/lib/context/HelpProvider/hooks/useHelpContext";
import { useUserData } from "@/lib/hooks/useUserData";

import styles from "./HelpWindow.module.scss";

import { Icon } from "../ui/Icon/Icon";

export const HelpWindow = (): JSX.Element => {
	const { t } = useTranslation(["contact"]);

	const { isVisible, setIsVisible } = useHelpContext();
	const [loadingOnboarded, setLoadingOnboarded] = useState(false);
	const helpWindowRef = useRef<HTMLDivElement>(null);
	const { userIdentityData } = useUserData();
	const { updateUserIdentity } = useUserApi();

	const closeHelpWindow = async () => {
		setIsVisible(false);
		if (userIdentityData && !userIdentityData.onboarded) {
			setLoadingOnboarded(true);
			await updateUserIdentity({
				...userIdentityData,
				username: userIdentityData.username,
				onboarded: true,
			});
		}
	};

	useEffect(() => {
		if (
			userIdentityData?.username &&
			!userIdentityData.onboarded &&
			!loadingOnboarded
		) {
			setIsVisible(true);
		}
	});

	useEffect(() => {
		const handleClickOutside = (event: MouseEvent) => {
			if (
				helpWindowRef.current &&
				!helpWindowRef.current.contains(event.target as Node)
			) {
				void (async () => {
					try {
						await closeHelpWindow();
					} catch (error) {
						console.error("Error while closing help window", error);
					}
				})();
			}
		};

		document.addEventListener("mousedown", handleClickOutside);

		return () => {
			document.removeEventListener("mousedown", handleClickOutside);
		};
	});

	return (
		<div
			className={`${styles.help_wrapper} ${isVisible ? styles.visible : ""}`}
			ref={helpWindowRef}
		>
			<div className={styles.header}>
				<span className={styles.title}>{t("help_window.title", { ns: "contact" })}</span>
				<Icon
					name="close"
					size="normal"
					color="black"
					handleHover={true}
					onClick={() => closeHelpWindow()}
				/>
			</div>
			<div className={styles.content}>
				<div className={styles.section}>
					<span className={styles.title}>{t("help_window.build_your_second_brains", { ns: "contact" })}</span>
					<span className={styles.section_content}>
						<strong>Brain</strong> {t("help_window.brain_description", { ns: "contact" })}
						<ul>
							<li>
								<strong>{t("help_window.knowledge_integration", { ns: "contact" })}</strong>
								<br />{t("help_window.connect_to_and_pull_data", { ns: "contact" })}
								<span className={styles.connection}>
									<strong>Google Drive</strong>{" "}
									<Image
										src="https://quivr-cms.s3.eu-west-3.amazonaws.com/gdrive_8316d080fd.png"
										alt="Google Drive"
										width={16}
										height={16}
									/>
								</span>
								,
								<span className={styles.connection}>
									<strong>SharePoint</strong>{" "}
									<Image
										src="https://quivr-cms.s3.eu-west-3.amazonaws.com/sharepoint_8c41cfdb09.png"
										alt="SharePoint"
										width={16}
										height={16}
									/>
								</span>
								,{" "}{t("help_window.and", { ns: "contact" })}
								<span className={styles.connection}>
									<strong className={styles.pre}>Dropbox</strong>{" "}
									<Image
										src="https://quivr-cms.s3.eu-west-3.amazonaws.com/dropbox_dce4f3d753.png"
										alt="Dropbox"
										width={16}
										height={16}
									/>
								</span>
								{t("help_window.you_can_also_incorporate_data_from", { ns: "contact" })} <strong>URLs</strong> {t("help_window.and", { ns: "contact" })} {" "}
								<strong>files</strong>.
							</li>
							<li>
								<strong>{t("help_window.ai_models", { ns: "contact" })}</strong>
								<br />{t("help_window.utilize_powerful_models", { ns: "contact" })}
								<strong>
									<em>GPT</em>
								</strong>{" "}
								{t("help_window.and", { ns: "contact" })} {" "}
								<strong>
									<em>Mistral</em>
								</strong>{" "}
								{t("help_window.to_process_and_understand", { ns: "contact" })}
							</li>
							<li>
								<strong>{t("help_window.customization", { ns: "contact" })}</strong>
								<br />{t("help_window.tailor_the_behavior", { ns: "contact" })}{" "}
								<em>{t("help_window.custom_prompts", { ns: "contact" })}</em> {t("help_window.and", { ns: "contact" })} <em>{t("help_window.settings", { ns: "contact" })}</em>, {t("help_window.such_as", { ns: "contact" })}{" "}
								<strong>{t("help_window.max_tokens", { ns: "contact" })}</strong>, {t("help_window.to_better_suit_your_needs", { ns: "contact" })}
							</li>
						</ul>
						<p>
							{t("help_window.you_can_also", { ns: "contact" })}<strong>{t("help_window.share", { ns: "contact" })}</strong> {t("help_window.your_brains_with_other_dobbie", { ns: "contact" })}
						</p>
					</span>
				</div>
				<div className={styles.section}>
					<span className={styles.title}>{t("help_window.talk_to_ai_models", { ns: "contact" })}</span>
					<span className={styles.section_content}>
						<p>
							{t("help_window.dobbie_allows_you_to", { ns: "contact" })}<strong>{t("help_window.interact_directly", { ns: "contact" })}</strong> {t("help_window.with_ai_models_such_as", { ns: "contact" })}
							<strong>
								<em>GPT-4</em>
							</strong>{" "}
							{t("help_window.and", { ns: "contact" })}
							<strong>
								<em>Mistral</em>
							</strong>
							{t("help_window.simply_start_conversation", { ns: "contact" })}
						</p>
					</span>
				</div>
				<div className={styles.section}>
					<div className={styles.title}>{t("help_window.select_assistant", { ns: "contact" })}</div>
					<span className={styles.section_content}>
						<p>
							{t("help_window.press", { ns: "contact" })}
							<strong> @</strong>{t("help_window.to_choose_the_AI_model", { ns: "contact" })}
						</p>
					</span>
					{/* <div className={styles.image}>
            <Image
              src="https://quivr-cms.s3.eu-west-3.amazonaws.com/Screen_82ac3783aa.png"
              width={500}
              height={100}
              alt="Dobbie"
            />
          </div> */}
				</div>
			</div>
		</div>
	);
};
