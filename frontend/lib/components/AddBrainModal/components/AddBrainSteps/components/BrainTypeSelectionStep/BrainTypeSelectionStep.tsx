import { iconList } from "@/lib/helpers/iconList";

import { BrainTypeSelection } from "./BrainTypeSelection/BrainTypeSelection";
import styles from "./BrainTypeSelectionStep.module.scss";

interface BrainType {
  name: string;
  description: string;
  iconName: keyof typeof iconList;
}

export const BrainTypeSelectionStep = (): JSX.Element => {
  const brainTypes: BrainType[] = [
    {
      name: "Core Brain",
      description: "Upload documents or website links to feed your brain.",
      iconName: "feed",
    },
    {
      name: "Sync Brain",
      description:
        "Connect to your tools and applications to interact with your data.",
      iconName: "software",
    },
    {
      name: "Custom Brain",
      description:
        "Explore your databases, converse with your APIs, and much more!",
      iconName: "custom",
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
