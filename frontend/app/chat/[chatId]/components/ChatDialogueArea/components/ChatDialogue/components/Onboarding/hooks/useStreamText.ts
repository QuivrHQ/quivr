import { useEffect, useState } from "react";

type UseStreamTextProps = {
  text: string;
  enabled?: boolean;
  shouldStream?: boolean;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useStreamText = ({
  text,
  enabled = true,
  shouldStream = true,
}: UseStreamTextProps) => {
  const [streamingText, setStreamingText] = useState<string>("");
  const [lastStreamIndex, setLastStreamIndex] = useState(0);

  const isDone = lastStreamIndex === text.length;

  const lastStream = !isDone ? text[lastStreamIndex] : "";

  useEffect(() => {
    if (!enabled) {
      setStreamingText("");

      return;
    }

    if (!shouldStream) {
      setStreamingText(text);
      setLastStreamIndex(text.length);

      return;
    }

    const messageInterval = setInterval(() => {
      if (lastStreamIndex < text.length) {
        setStreamingText(
          (prevText) => prevText + (text[lastStreamIndex] ?? "")
        );
        setLastStreamIndex((prevIndex) => prevIndex + 1);
      } else {
        clearInterval(messageInterval);
      }
    }, 30);

    return () => {
      clearInterval(messageInterval);
    };
  }, [text, lastStreamIndex, enabled, shouldStream]);

  return { streamingText, isDone, lastStream };
};
