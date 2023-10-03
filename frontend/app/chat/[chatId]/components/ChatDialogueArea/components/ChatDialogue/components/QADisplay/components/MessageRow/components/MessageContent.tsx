import ReactMarkdown from "react-markdown";

export const MessageContent = ({
  text,
  markdownClasses,
}: {
  text: string;
  markdownClasses: string;
}): JSX.Element => (
  <div data-testid="chat-message-text">
    <ReactMarkdown className={markdownClasses}>{text}</ReactMarkdown>
  </div>
);
