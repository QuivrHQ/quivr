type BrainSuggestionProps = {
  content: string;
  id: string;
};
export const BrainSuggestion = ({
  content,
  id,
}: BrainSuggestionProps): JSX.Element => {
  //TODO: use this id for ShareBrain component
  console.log({ id });

  return (
    <div className="relative flex group items-center">
      <div
        className={
          "flex flex-1 items-center gap-2 w-full text-left px-5 py-2 text-sm leading-5 text-gray-900 dark:text-gray-300 group-hover:bg-gray-100 dark:group-hover:bg-gray-700 group-focus:bg-gray-100 dark:group-focus:bg-gray-700 group-focus:outline-none transition-colors"
        }
      >
        <span className="flex-1">{content}</span>
      </div>
    </div>
  );
};
