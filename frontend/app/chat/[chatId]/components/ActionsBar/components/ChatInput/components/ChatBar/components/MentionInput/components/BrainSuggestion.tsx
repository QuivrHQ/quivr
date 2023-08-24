type BrainSuggestionProps = {
  content: string;
};
export const BrainSuggestion = ({
  content,
}: BrainSuggestionProps): JSX.Element => {
  return <span>{content}</span>;
};
