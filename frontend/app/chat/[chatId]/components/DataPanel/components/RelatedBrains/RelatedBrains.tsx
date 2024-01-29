import { useEffect, useState } from "react";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import Icon from "@/lib/components/ui/Icon/Icon";
import { useChatContext } from "@/lib/context";
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

  return (
    <FoldableSection
      label="Related Brains (Beta)"
      icon="brain"
      foldedByDefault={closeBrains?.length === 0}
    >
      <div className={styles.close_brains_wrapper}>
        {closeBrains?.map((brain, index) => (
          <div className={styles.brain_line} key={index}>
            <div className={styles.left}>
              <div className={styles.copy_icon}>
                <Icon
                  name="copy"
                  size="normal"
                  color="black"
                  handleHover={true}
                  onClick={() =>
                    void navigator.clipboard.writeText("@" + brain.name)
                  }
                ></Icon>
              </div>
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
            </div>
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
