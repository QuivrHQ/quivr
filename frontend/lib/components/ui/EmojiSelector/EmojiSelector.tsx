// components/EmojiSelector.tsx
import { EmojiClickData } from "emoji-picker-react";
import dynamic from "next/dynamic";

const EmojiPicker = dynamic(() => import("emoji-picker-react"), { ssr: false });

const EmojiSelector = ({
  onSelectEmoji,
}: {
  onSelectEmoji?: (emoji: string) => void;
}): JSX.Element => {
  const onEmojiClick = (emojiObject: EmojiClickData) => {
    if (onSelectEmoji) {
      onSelectEmoji(emojiObject.emoji);
    }
  };

  return <EmojiPicker onEmojiClick={onEmojiClick} />;
};

export default EmojiSelector;
