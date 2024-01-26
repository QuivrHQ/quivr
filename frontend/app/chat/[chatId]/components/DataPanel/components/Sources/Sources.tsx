import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";

interface SourcesProps {
  sources?: [string];
}

const Sources = ({ sources }: SourcesProps): JSX.Element => {
  return (
    <FoldableSection label="Sources" icon="file">
      {sources?.map((source, index) => (
        <div key={index}>{source}</div>
      ))}
    </FoldableSection>
  );
};

export default Sources;
