import { Fragment } from "react";

type QuestionBrainProps = {
  brainName?: string | null;
};
export const QuestionBrain = ({
  brainName,
}: QuestionBrainProps): JSX.Element => {
  if (brainName === undefined || brainName === null) {
    return <Fragment />;
  }

  return (
    <span data-testid="brain-tags" className="text-gray-400 mb-1 text-xs">
      @{brainName}
    </span>
  );
};
