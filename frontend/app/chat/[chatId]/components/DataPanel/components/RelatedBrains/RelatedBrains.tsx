import { useEffect, useState } from "react";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { useChatContext } from "@/lib/context";
import { CloseBrain } from "@/lib/types/MessageMetadata";

import styles from "./RelatedBrains.module.scss";

interface RelatedBrainsProps {
  closeBrains: CloseBrain[];
}

interface CloseBrainProps {
  color: string;
  isCurrentBrain: boolean;
}

const RelatedBrains = ({ closeBrains }: RelatedBrainsProps): JSX.Element => {
  const [closeBrainsProps, setCloseBrainProps] = useState<CloseBrainProps[]>(
    []
  );
  const { messages } = useChatContext();
  const lerp = (start: number, end: number, t: number): number => {
    return start * (1 - t) + end * t;
  };

  useEffect(() => {
    const newProps = closeBrains.map((brain) => {
      const t = Math.pow(brain.similarity, 2);
      const r = Math.round(lerp(211, 138, t));
      const g = Math.round(lerp(211, 43, t));
      const b = Math.round(lerp(211, 226, t));
      const isCurrentBrain =
        brain.name === messages[messages.length - 1].brain_name;

      console.info(messages);

      return { color: `rgb(${r}, ${g}, ${b})`, isCurrentBrain: isCurrentBrain };
    });
    setCloseBrainProps(newProps);
    console.info(newProps);
  }, [closeBrains, messages]);

  if (closeBrains.length === 0) {
    return <></>;
  }

  return (
    <FoldableSection
      label="Related Brains (Beta)"
      icon="brain"
      foldedByDefault={true}
    >
      <div className={styles.close_brains_wrapper}>
        {closeBrains.map((brain, index) => (
          <div className={styles.brain_line} key={index}>
            <p
              className={`
              ${styles.brain_name ?? ""} 
              ${
                closeBrainsProps[index]?.isCurrentBrain
                  ? styles.current ?? ""
                  : ""
              }
              `}
            >
              @{brain.name}
            </p>
            <p
              className={styles.brain_score}
              style={{ color: closeBrainsProps[index]?.color }}
            >
              {Math.round(brain.similarity * 100)}
            </p>
          </div>
        ))}
      </div>
    </FoldableSection>
  );
};

export default RelatedBrains;
