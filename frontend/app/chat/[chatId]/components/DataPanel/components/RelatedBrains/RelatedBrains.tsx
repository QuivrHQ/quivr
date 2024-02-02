import { UUID } from "crypto";
import { useEffect, useState } from "react";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { useChatContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { CloseBrain } from "@/lib/types/MessageMetadata";

import styles from "./RelatedBrains.module.scss";

interface RelatedBrainsProps {
  closeBrains?: CloseBrain[];
}

interface CloseBrainProps {
  color: string;
  isCurrentBrain: boolean;
}

const RelatedBrains = ({ closeBrains }: RelatedBrainsProps): JSX.Element => {
  const { setCurrentBrainId } = useBrainContext();
  const [closeBrainsProps, setCloseBrainProps] = useState<CloseBrainProps[]>(
    []
  );
  const { messages } = useChatContext();
  const lerp = (start: number, end: number, t: number): number => {
    return start * (1 - t) + end * t;
  };

  useEffect(() => {
    if (closeBrains) {
      const newProps = closeBrains.map((brain) => {
        const t = Math.pow(brain.similarity, 2);
        const r = Math.round(lerp(211, 138, t));
        const g = Math.round(lerp(211, 43, t));
        const b = Math.round(lerp(211, 226, t));
        const isCurrentBrain =
          brain.id === messages[messages.length - 1]?.brain_id;

        return {
          color: `rgb(${r}, ${g}, ${b})`,
          isCurrentBrain: isCurrentBrain,
        };
      });
      setCloseBrainProps(newProps);
    }
  }, [closeBrains, messages.length]);

  const setCurrentBrain = (index: number) => {
    if (closeBrains?.[index]) {
      setCurrentBrainId(closeBrains[index].id as UUID);
      closeBrainsProps.forEach((_closeBrains, closeBrainIndex) => {
        closeBrainsProps[closeBrainIndex].isCurrentBrain =
          index === closeBrainIndex;
      });
    }
  };

  return (
    <FoldableSection
      label="Related Brains (Beta)"
      icon="brain"
      // When related brains are fixed, foldedByDefault={closeBrains?.length === 0}
      foldedByDefault={true}
    >
      <div className={styles.close_brains_wrapper}>
        {closeBrains?.map((brain, index) => (
          <div className={styles.brain_line} key={index}>
            <span
              className={`
              ${styles.brain_name ?? ""} 
              ${
                closeBrainsProps[index]?.isCurrentBrain
                  ? styles.current ?? ""
                  : ""
              }
              `}
              onClick={() => void setCurrentBrain(index)}
            >
              {brain.name}
            </span>
            <div
              className={styles.similarity_score}
              title="Similarity score"
              style={{ color: closeBrainsProps[index]?.color }}
            >
              {Math.round(brain.similarity * 100)}
            </div>
          </div>
        ))}
      </div>
    </FoldableSection>
  );
};

export default RelatedBrains;
