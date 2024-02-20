import Image from "next/image";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";

import styles from "./CustomBrainList.module.scss";

import { useBrainCreationContext } from "../../../brainCreation-provider";

export const CustomBrainList = ({
  customBrainList,
}: {
  customBrainList: IntegrationBrains[];
}): JSX.Element => {
  const { setCurrentIntegrationBrain, currentIntegrationBrain } =
    useBrainCreationContext();

  return (
    <div className={styles.cards_wrapper}>
      <MessageInfoBox content="More custom brains are coming!" type="info" />
      <span className={styles.title}>Choose a custom brain</span>
      <div>
        {customBrainList.map((brain) => {
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
