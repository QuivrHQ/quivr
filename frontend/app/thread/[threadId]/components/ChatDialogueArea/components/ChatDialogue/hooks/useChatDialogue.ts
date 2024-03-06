import _debounce from "lodash/debounce";
import { useCallback, useEffect, useRef } from "react";

import { useThread } from "@/app/thread/[threadId]/hooks/useThread";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

//TODO: link this to thread input to get the right height
const threadInputHeightEstimation = 100;

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThreadDialogue = () => {
  const threadListRef = useRef<HTMLDivElement | null>(null);
  const { messages } = useThread();
  const { shouldDisplayFeedCard } = useKnowledgeToFeedContext();

  const scrollToBottom = useCallback(
    _debounce(() => {
      if (threadListRef.current) {
        threadListRef.current.scrollTo({
          top: threadListRef.current.scrollHeight,
          behavior: "auto",
        });
      }
    }, 100),
    []
  );

  useEffect(() => {
    const computeCardHeight = () => {
      if (threadListRef.current) {
        const cardTop = threadListRef.current.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        const cardHeight = windowHeight - cardTop - threadInputHeightEstimation;
        threadListRef.current.style.height = `${cardHeight}px`;
      }
    };

    computeCardHeight();
    window.addEventListener("resize", computeCardHeight);

    return () => {
      window.removeEventListener("resize", computeCardHeight);
    };
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom, shouldDisplayFeedCard]);

  return {
    threadListRef,
  };
};
