import Prism from "prismjs";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";

import styles from "./MessageContent.module.scss";

export const MessageContent = ({
  text,
  isUser,
  hide,
}: {
  text: string;
  isUser: boolean;
  hide: boolean;
}): JSX.Element => {
  const [showLog] = useState(true);
  const [isLog, setIsLog] = useState(true);

  const extractLog = (log: string) => {
    const logRegex = /🧠<([^>]+)>🧠/g;
    const logs = [];
    let match;

    while ((match = logRegex.exec(log))) {
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

    Prism.highlightAll(); // Si vous utilisez Prism.js
  }, [text]);

  const { logs, cleanedText } = extractLog(text);

  console.info(cleanedText);

  return (
    <div
      className={hide && !isUser ? styles.hiden : ""}
      data-testid="chat-message-text"
    >
      {isLog && showLog && logs.length > 0 && (
        <div
          className={`${styles.logContainer} text-xs text-white p-2 rounded`}
        >
          <ReactMarkdown remarkPlugins={[gfm]}>{logs}</ReactMarkdown>
        </div>
      )}
      <ReactMarkdown
        className={`
          ${styles.markdown} 
          ${isUser ? styles.user : styles.brain}
          ${cleanedText === "🧠" ? styles.thinking : ""} 
        `}
        remarkPlugins={[gfm]}
      >
        {cleanedText}
      </ReactMarkdown>
    </div>
  );
};
