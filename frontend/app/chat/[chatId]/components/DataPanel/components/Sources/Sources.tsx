import { useEffect } from "react";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { Source } from "@/lib/types/MessageMetadata";

interface SourcesProps {
  sources?: Source[];
}

const Sources = ({ sources }: SourcesProps): JSX.Element => {
  useEffect(() => {
    console.info(sources);
  }, [sources]);

  return (
    <FoldableSection label="Sources" icon="file">
      {sources?.map((source, index) => (
        <a
          href={source.source_url}
          key={index}
          target="_blank"
          rel="noopener noreferrer"
        >
          <div>{source.name}</div>
        </a>
      ))}
    </FoldableSection>
  );
};

export default Sources;
