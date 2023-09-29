import _debounce from "lodash/debounce";
import { useCallback, useEffect, useRef } from "react";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useKnowledgeToFeedContext } from "@/lib/context/KnowledgeToFeedProvider/hooks/useKnowledgeToFeedContext";

//TODO: link this to chat input to get the right height
const chatInputHeightEstimation = 100;

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatDialogue = () => {
  const chatListRef = useRef<HTMLDivElement | null>(null);
  const { messages } = useChat();
  const { shouldDisplayFeedCard } = useKnowledgeToFeedContext();

  const scrollToBottom = useCallback(
    _debounce(() => {
      if (chatListRef.current) {
        chatListRef.current.scrollTo({
          top: chatListRef.current.scrollHeight,
          behavior: "auto",
        });
      }
    }, 100),
    []
  );

  useEffect(() => {
    const computeCardHeight = () => {
      if (chatListRef.current) {
        const cardTop = chatListRef.current.getBoundingClientRect().top;
        const windowHeight = window.innerHeight;
        const cardHeight = windowHeight - cardTop - chatInputHeightEstimation;
        chatListRef.current.style.height = `${cardHeight}px`;
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
    chatListRef,
  };
};
