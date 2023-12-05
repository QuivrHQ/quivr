type PromptSuggestionProps = {
  content: string;
};
export const PromptSuggestion = ({
  content,
}: PromptSuggestionProps): JSX.Element => {
  return (
    <div className="flex flex-1 flex-row gap-2 w-full text-left px-5 py-2 text-sm text-gray-900 dark:text-gray-300">
      <div className="flex flex-1">
        <span>{content}</span>
      </div>
    </div>
  );
};
