import Image from "next/image";

import { IntegrationBrains } from "@/lib/api/brain/types";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";

import styles from "./CustomBrainList.module.scss";

import { useBrainCreationContext } from "../../../brainCreation-provider";

export const CustomBrainList = ({
  customBrainList,
}: {
  customBrainList: IntegrationBrains[];
}): JSX.Element => {
  const { setCurrentIntegrationBrain } = useBrainCreationContext();

  return (
    <div className={styles.cards_wrapper}>
      {customBrainList.map((brain) => {
        return (
          <div
            className={styles.card_container}
            key={brain.id}
            onClick={() => setCurrentIntegrationBrain(brain)}
          >
            <div className={styles.icon_help}>
              <Tooltip tooltip={brain.description}>
                <div>
                  <Icon
                    color="black"
                    handleHover={true}
                    size="normal"
                    name="help"
                  />
                </div>
              </Tooltip>
            </div>
            <div className={styles.brain_card_wrapper}>
              <span className={styles.brain_title}>
                {brain.integration_name}
              </span>
              <Image
                src={brain.integration_logo_url}
                alt={brain.integration_name}
                width={70}
                height={70}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
};
