import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

export const MessageContent = ({
  text,
  isUser,
  markdownClasses,
}: {
  text: string;
  isUser: boolean;
  markdownClasses: string;
}): JSX.Element => {
  const [showLog] = useState(true);
  const [isLog, setIsLog] = useState(true);

  const extractLog = (log: string) => {
    const logRegex = /🧠<([^>]+)>🧠/g;
    const logs = [];
    let match;

    while ((match = logRegex.exec(log))) {
      // Add two spaces and a newline for markdown line break
      // eslint-disable-next-line @typescript-eslint/restrict-plus-operands
      logs.push("- " + match[1] + "  \n");
    }

    return {
      logs: logs.join(""), // Join with empty string, each log already has newline
      cleanedText: log.replace(logRegex, ""),
    };
  };

  useEffect(() => {
    if (text.includes("🧠<")) {
      setIsLog(true);
    } else {
      setIsLog(false);
    }
    console.info(isUser);
  }, [text]);

  const { logs, cleanedText } = extractLog(text);

  return (
    <div data-testid="chat-message-text">
      {isLog && showLog && logs.length > 0 && (
        <div className="text-xs text-white-600 p-2 rounded">
          <ReactMarkdown>{logs}</ReactMarkdown>
        </div>
      )}
      <ReactMarkdown className={`text-base ${markdownClasses}`}>
        {cleanedText}
      </ReactMarkdown>
    </div>
  );
};
