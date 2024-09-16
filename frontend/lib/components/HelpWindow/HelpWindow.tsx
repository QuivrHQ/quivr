import Image from "next/image";
import { useEffect, useRef, useState } from "react";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { useHelpContext } from "@/lib/context/HelpProvider/hooks/useHelpContext";
import { useUserData } from "@/lib/hooks/useUserData";

import styles from "./HelpWindow.module.scss";

import { Icon } from "../ui/Icon/Icon";

export const HelpWindow = (): JSX.Element => {
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
        <span className={styles.title}>🧠 What is Quivr ?</span>
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
          <span className={styles.title}>🧱 Build your second brains</span>
          <span className={styles.section_content}>
            A <strong>Brain</strong> in Quivr is an advanced knowledge system
            designed to integrate and leverage information from various sources.
            <ul>
              <li>
                <strong>📁 Knowledge Integration</strong>
                <br /> Connect to and pull data from various platforms like{" "}
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
                , and{""}
                <span className={styles.connection}>
                  <strong className={styles.pre}> Dropbox</strong>{" "}
                  <Image
                    src="https://quivr-cms.s3.eu-west-3.amazonaws.com/dropbox_dce4f3d753.png"
                    alt="Dropbox"
                    width={16}
                    height={16}
                  />
                </span>
                . You can also incorporate data from <strong>URLs</strong> and{" "}
                <strong>files</strong>.
              </li>
              <li>
                <strong>🤖 AI Models</strong>
                <br /> Utilize powerful models such as{" "}
                <strong>
                  <em>GPT</em>
                </strong>{" "}
                and{" "}
                <strong>
                  <em>Mistral</em>
                </strong>{" "}
                to process and understand the integrated knowledge.
              </li>
              <li>
                <strong>🔧 Customization</strong>
                <br /> Tailor the behavior of your Brain with{" "}
                <em>custom prompts</em> and <em>settings</em>, such as{" "}
                <strong>max tokens</strong>, to better suit your needs.
              </li>
            </ul>
            <p>
              You can also <strong>share</strong> your brains with other Quivr
              users, allowing them to access and benefit from your knowledge
              systems. 🤝
            </p>
          </span>
        </div>
        <div className={styles.section}>
          <span className={styles.title}>🤖 Talk to AI Models</span>
          <span className={styles.section_content}>
            <p>
              Quivr allows you to <strong>interact directly</strong> with AI
              models such as{" "}
              <strong>
                <em>GPT-4</em>
              </strong>{" "}
              and{" "}
              <strong>
                <em>Mistral</em>
              </strong>
              . Simply start a conversation with the AI to get answers and
              support based on a broad range of data and knowledge. 🤖✨
            </p>
          </span>
        </div>
        <div className={styles.section}>
          <div className={styles.title}>🎯 Select assistant</div>
          <span className={styles.section_content}>
            <p>
              Press
              <strong> @</strong> to choose the AI model or the Brain you want
              to interact with.
            </p>
          </span>
          <div className={styles.image}>
            <Image
              src="https://quivr-cms.s3.eu-west-3.amazonaws.com/Screen_82ac3783aa.png"
              width={500}
              height={100}
              alt="Quivr"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
