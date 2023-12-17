import { useEffect, useRef, useState } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useSuggestionsOverflowHandler = () => {
  const [shouldShowScrollToBottomIcon, setShouldShowScrollToBottomIcon] =
    useState(false);

  const suggestionsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const scrollContainer = suggestionsRef.current;
    const handleScroll = () => {
      if (scrollContainer === null) {
        return;
      }
      const SCROLL_POSITION_NOISE = 10;
      const asReachedBottom =
        scrollContainer.scrollHeight -
          scrollContainer.scrollTop -
          SCROLL_POSITION_NOISE <=
        scrollContainer.clientHeight;

      setShouldShowScrollToBottomIcon(!asReachedBottom);
    };
    scrollContainer?.addEventListener("scroll", handleScroll);

    return () => {
      scrollContainer?.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const scrollToBottom = () => {
    if (suggestionsRef.current) {
      suggestionsRef.current.scrollTo({
        top: suggestionsRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  };

  return {
    shouldShowScrollToBottomIcon,
    scrollToBottom,
    suggestionsRef,
  };
};
