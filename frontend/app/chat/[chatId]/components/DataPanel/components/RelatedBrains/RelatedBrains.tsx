import { useEffect, useState } from "react";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { CloseBrain } from "@/lib/types/MessageMetadata";

import styles from "./RelatedBrains.module.scss";

interface RelatedBrainsProps {
  closeBrains: CloseBrain[];
}

const RelatedBrains = ({ closeBrains }: RelatedBrainsProps): JSX.Element => {
  const [colors, setColors] = useState<string[]>([]);
  const lerp = (start: number, end: number, t: number): number => {
    return start * (1 - t) + end * t;
  };

  useEffect(() => {
    const newColors = closeBrains.map((brain) => {
      const t = Math.pow(brain.similarity, 2);
      const r = Math.round(lerp(211, 138, t));
      const g = Math.round(lerp(211, 43, t));
      const b = Math.round(lerp(211, 226, t));

      return `rgb(${r}, ${g}, ${b})`;
    });
    setColors(newColors);
  }, [closeBrains]);

  if (closeBrains.length === 0) {
    return <></>;
  }

  return (
    <FoldableSection
      label="Related Brains (Beta)"
      icon="brain"
      foldedByDefault={true}
    >
      {closeBrains.map((brain, index) => (
        <div className={styles.brain_line} key={index}>
          <p className={styles.brain_name}>@{brain.name}</p>
          <p className={styles.brain_score} style={{ color: colors[index] }}>
            {Math.round(brain.similarity * 100)}
          </p>
        </div>
      ))}
    </FoldableSection>
  );
};

export default RelatedBrains;
