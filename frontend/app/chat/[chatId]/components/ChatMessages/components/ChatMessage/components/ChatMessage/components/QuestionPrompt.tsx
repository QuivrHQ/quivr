import { Fragment } from "react";

type QuestionProptProps = {
  promptName?: string | null;
};
export const QuestionPrompt = ({
  promptName,
}: QuestionProptProps): JSX.Element => {
  if (promptName === undefined || promptName === null) {
    return <Fragment />;
  }

  return (
    <span data-testid="prompt-tags" className="text-gray-400 mb-1 text-xs">
      #{promptName}
    </span>
  );
};
