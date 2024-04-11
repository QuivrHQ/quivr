import { IntegrationBrains } from "@/lib/api/brain/types";
import { BrainCard } from "@/lib/components/ui/BrainCard/BrainCard";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { useUserData } from "@/lib/hooks/useUserData";

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
  const { userIdentityData } = useUserData();

  return (
    <div className={styles.cards_wrapper}>
      <MessageInfoBox type="info">
        <span>
          A Brain is a specialized AI tool designed to interact with specific
          use cases or data sources.
        </span>
      </MessageInfoBox>
      {!userIdentityData?.onboarded && (
        <MessageInfoBox type="tutorial">
          <span>
            Let&apos;s start by creating a Docs &amp; URLs brain.<br></br>Of
            course, feel free to explore other types of brains during your Quivr
            journey.
          </span>
        </MessageInfoBox>
      )}
      <span className={styles.title}>Choose a brain type</span>
      <div className={styles.brains_grid}>
        {brains.map((brain) => {
          return (
            <BrainCard
              tooltip={brain.description}
              brainName={brain.integration_display_name}
              tags={brain.tags}
              selected={currentSelectedBrain?.id === brain.id}
              imageUrl={brain.integration_logo_url}
              callback={() => {
                next();
                setCurrentSelectedBrain(brain);
              }}
              key={brain.id}
              disabled={!userIdentityData?.onboarded && !brain.onboarding_brain}
            />
          );
        })}
      </div>
    </div>
  );
};
