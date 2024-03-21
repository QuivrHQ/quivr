import { capitalCase } from "change-case";
import Image from "next/image";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { Tag } from "@/lib/components/ui/Tag/Tag";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./BrainCatalogue.module.scss";

import { useBrainCreationContext } from "../../../brainCreation-provider";

export const BrainCatalogue = ({
  brains,
  next,
}: {
  brains: IntegrationBrains[];
  next: () => void;
}): JSX.Element => {
  const { setCurrentSelectedBrain, currentSelectedBrain } =
    useBrainCreationContext();
  const { isDarkMode } = useUserSettingsContext();

  return (
    <div className={styles.cards_wrapper}>
      <MessageInfoBox type="info">
        <span>
          A Brain is a specialized AI tool designed to interact with specific
          use cases or data sources.
        </span>
      </MessageInfoBox>
      <span className={styles.title}>Choose a brain type</span>
      <div className={styles.brains_grid}>
        {brains.map((brain) => {
          return (
            <div
              key={brain.id}
              className={styles.brain_card_container}
              onClick={() => {
                next();
                setCurrentSelectedBrain(brain);
              }}
            >
              <Tooltip tooltip={brain.description}>
                <div
                  className={`${styles.brain_card_wrapper} ${
                    currentSelectedBrain === brain ? styles.selected : ""
                  }`}
                >
                  <Image
                    className={isDarkMode ? styles.dark_image : ""}
                    src={brain.integration_logo_url}
                    alt={brain.integration_name}
                    width={50}
                    height={50}
                  />
                  <span className={styles.brain_title}>
                    {brain.integration_display_name}
                  </span>
                  <div className={styles.tag_wrapper}>
                    {brain.tags[0] && (
                      <Tag color="primary" name={capitalCase(brain.tags[0])} />
                    )}
                  </div>
                </div>
              </Tooltip>
            </div>
          );
        })}
      </div>
    </div>
  );
};
