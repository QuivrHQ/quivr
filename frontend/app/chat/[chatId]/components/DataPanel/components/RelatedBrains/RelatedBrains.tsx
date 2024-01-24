import { CloseBrain } from "@/lib/types/MessageMetadata";

import styles from "./RelatedBrains.module.scss";

interface RelatedBrainsProps {
  closeBrains: CloseBrain[];
}

const RelatedBrains = ({ closeBrains }: RelatedBrainsProps): JSX.Element => {
  return (
    <div className={styles.related_brains_wrapper}>
      {closeBrains.map((brain, index) => (
        <div key={index}>
          <p>Brain: {brain.name}</p>
          <p>Similarity: {brain.similarity}</p>
        </div>
      ))}
    </div>
  );
};

export default RelatedBrains;
