import { Editor } from "./Editor/Editor";

type ThreadEditorProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
};
export const ThreadEditor = ({
  onSubmit,
  setMessage,
  message,
}: ThreadEditorProps): JSX.Element => (
  <Editor onSubmit={onSubmit} setMessage={setMessage} message={message} />
);
