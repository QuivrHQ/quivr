type UseMessageRowProps = {
  speaker: "user" | "assistant";
  text?: string;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMessageRow = ({ speaker, text }: UseMessageRowProps) => {
  const isUserSpeaker = speaker === "user";

  const handleCopy = () => {
    if (text === undefined) {
      return;
    }
    navigator.clipboard.writeText(text).catch((err) => console.error(err));
  };

  return {
    isUserSpeaker,
    handleCopy,
  };
};
