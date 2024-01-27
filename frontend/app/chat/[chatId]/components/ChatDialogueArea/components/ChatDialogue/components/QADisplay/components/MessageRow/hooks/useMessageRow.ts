import { useState } from "react";

type UseMessageRowProps = {
  speaker: "user" | "assistant";
  text?: string;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMessageRow = ({ speaker, text }: UseMessageRowProps) => {
  const isUserSpeaker = speaker === "user";
  const [isCopied, setIsCopied] = useState(false);

  const handleCopy = () => {
    if (text === undefined) {
      return;
    }
    navigator.clipboard.writeText(text).then(
      () => setIsCopied(true),
      (err) => console.error("Failed to copy!", err)
    );
    setTimeout(() => setIsCopied(false), 2000); // Reset after 2 seconds
  };

  return {
    isUserSpeaker,
    isCopied,
    handleCopy,
  };
};
