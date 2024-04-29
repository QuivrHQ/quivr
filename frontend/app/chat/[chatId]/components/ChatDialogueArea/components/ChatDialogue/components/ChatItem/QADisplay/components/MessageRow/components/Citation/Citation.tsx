import { CitationType } from "../../types/types";

type CitationProps = {
  citation: CitationType;
};
export const Citation = ({ citation }: CitationProps): JSX.Element => {
  return (
    <div>
      <p>{citation.filename}</p>
    </div>
  );
};
