import Prism from "prismjs";
import "prismjs/components/prism-c";
import "prismjs/components/prism-cpp";
import "prismjs/components/prism-csharp";
import "prismjs/components/prism-go";
import "prismjs/components/prism-java";
import "prismjs/components/prism-markup";
import "prismjs/components/prism-python";
import "prismjs/components/prism-rust";
import "prismjs/components/prism-typescript";
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import gfm from "remark-gfm";

import Icon from "@/lib/components/ui/Icon/Icon";

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
      logs: logs.join(""),
      cleanedText: log.replace(logRegex, ""),
    };
  };

  useEffect(() => {
    if (text.includes("🧠<")) {
      setIsLog(true);
    } else {
      setIsLog(false);
    }

    Prism.highlightAll();
  }, [text]);

  const { logs, cleanedText } = extractLog(text);

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
        components={{
          code: ({ className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className ?? "");

            return match ? (
              <div className={styles.code_block}>
                <div
                  className={styles.icon}
                  onClick={() => {
                    void navigator.clipboard.writeText(String(children));
                  }}
                >
                  <Icon
                    name="copy"
                    size="small"
                    color="black"
                    handleHover={true}
                  />
                </div>
                <pre className={className}>
                  <code
                    {...props}
                    dangerouslySetInnerHTML={{
                      __html: Prism.highlight(
                        String(children).trim(),
                        // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
                        Prism.languages[match[1]],
                        match[1]
                      ),
                    }}
                  />
                </pre>
              </div>
            ) : (
              <code {...props} className={className}>
                {children}
              </code>
            );
          },
        }}
      >
        {cleanedText}
      </ReactMarkdown>
    </div>
  );
};
