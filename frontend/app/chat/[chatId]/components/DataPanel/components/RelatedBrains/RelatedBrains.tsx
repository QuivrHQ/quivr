import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { CloseBrain } from "@/lib/types/MessageMetadata";

import styles from "./RelatedBrains.module.scss";

interface RelatedBrainsProps {
  closeBrains: CloseBrain[];
}

const RelatedBrains = ({ closeBrains }: RelatedBrainsProps): JSX.Element => {
  return (
    <div className={styles.related_brains_wrapper}>
      <FoldableSection label="Related Brains" icon="brain">
        {closeBrains.map((brain, index) => (
          <div key={index}>
            <p>Brain: {brain.name}</p>
            <p>Similarity: {brain.similarity}</p>
          </div>
        ))}
      </FoldableSection>
    </div>
  );
};

export default RelatedBrains;
