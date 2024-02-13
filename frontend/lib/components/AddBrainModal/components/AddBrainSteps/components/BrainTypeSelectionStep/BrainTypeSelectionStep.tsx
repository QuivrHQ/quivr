import { BrainType } from "@/lib/components/AddBrainModal/types/types";

import { BrainTypeSelection } from "./BrainTypeSelection/BrainTypeSelection";
import styles from "./BrainTypeSelectionStep.module.scss";

export const BrainTypeSelectionStep = (): JSX.Element => {
  const brainTypes: BrainType[] = [
    {
      name: "Core Brain",
      description: "Upload documents or website links to feed your brain.",
      iconName: "feed",
    },
    {
      name: "Sync Brain - Coming soon!",
      description:
        "Connect to your tools and applications to interact with your data.",
      iconName: "software",
      disabled: true,
    },
    {
      name: "Custom Brain - Coming soon!",
      description:
        "Explore your databases, converse with your APIs, and much more!",
      iconName: "custom",
      disabled: true,
    },
  ];

  return (
    <div className={styles.brain_types_wrapper}>
      <span className={styles.title}>Choose a type of brain</span>
      {brainTypes.map((brainType, index) => (
        <div key={index} className={styles.brain_type}>
          <BrainTypeSelection brainType={brainType} />
        </div>
      ))}
    </div>
  );
};
