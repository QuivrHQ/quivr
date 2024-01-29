import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { Source } from "@/lib/types/MessageMetadata";

import styles from "./Sources.module.scss";

interface SourcesProps {
  sources?: Source[];
}

const Sources = ({ sources }: SourcesProps): JSX.Element => {
  return (
    <FoldableSection
      label="Sources"
      icon="file"
      foldedByDefault={sources?.length === 0}
    >
      <div className={styles.sources_wrapper}>
        {sources?.map((source, index) => (
          <div className={styles.source_wrapper} key={index}>
            <a
              href={source.source_url}
              key={index}
              target="_blank"
              rel="noopener noreferrer"
            >
              <div className={styles.source}>{source.name}</div>
            </a>
          </div>
        ))}
      </div>
    </FoldableSection>
  );
};

export default Sources;
