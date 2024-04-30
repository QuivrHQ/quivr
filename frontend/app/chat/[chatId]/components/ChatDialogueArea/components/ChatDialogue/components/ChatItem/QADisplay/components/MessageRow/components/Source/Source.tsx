import { SourceFile } from "../../types/types";

type SourceProps = {
  sourceFile: SourceFile;
};
export const SourceCitations = ({ sourceFile }: SourceProps): JSX.Element => {
  return <div>{sourceFile.filename}</div>;
};
