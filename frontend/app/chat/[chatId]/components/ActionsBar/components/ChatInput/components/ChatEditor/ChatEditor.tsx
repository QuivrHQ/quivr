import { Editor } from "./components/Editor/Editor";

type ChatEditorProps = {
  onSubmit: () => void;
  setMessage: (text: string) => void;
  message: string;
};
export const ChatEditor = ({
  onSubmit,
  setMessage,
  message,
}: ChatEditorProps): JSX.Element => (
  <Editor onSubmit={onSubmit} setMessage={setMessage} message={message} />
);
