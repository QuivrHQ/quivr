import Image from "next/image";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";

import styles from "./BrainCatalogue.module.scss";

import { useBrainCreationContext } from "../../../brainCreation-provider";

export const BrainCatalogue = ({
  brains,
}: {
  brains: IntegrationBrains[];
}): JSX.Element => {
  const { setCurrentIntegrationBrain, currentIntegrationBrain } =
    useBrainCreationContext();

  return (
    <div className={styles.cards_wrapper}>
      <MessageInfoBox type="info">More brains are coming!</MessageInfoBox>
      <span className={styles.title}>Choose a brain</span>
      <div>
        {brains.map((brain) => {
          return (
            <div
              key={brain.id}
              onClick={() => setCurrentIntegrationBrain(brain)}
            >
              <Tooltip tooltip={brain.description}>
                <div
                  className={`${styles.brain_card_wrapper} ${
                    currentIntegrationBrain === brain ? styles.selected : ""
                  }`}
                >
                  <Image
                    src={brain.integration_logo_url}
                    alt={brain.integration_name}
                    width={50}
                    height={50}
                  />
                  <span className={styles.brain_title}>
                    {brain.integration_name}
                  </span>
                </div>
              </Tooltip>
            </div>
          );
        })}
      </div>
    </div>
  );
};
