// components/EmojiSelector.tsx
import { EmojiClickData, Theme } from "emoji-picker-react";
import dynamic from "next/dynamic";

import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useDevice } from "@/lib/hooks/useDevice";

import styles from "./EmojiSelector.module.scss";

const EmojiPicker = dynamic(() => import("emoji-picker-react"), { ssr: false });

const EmojiSelector = ({
  onSelectEmoji,
}: {
  onSelectEmoji?: (emoji: string) => void;
}): JSX.Element => {
  const { isDarkMode } = useUserSettingsContext();
  const { isMobile } = useDevice();

  const onEmojiClick = (emojiObject: EmojiClickData) => {
    if (onSelectEmoji) {
      onSelectEmoji(emojiObject.emoji);
    }
  };

  return (
    <div className={styles.emoji_picker_wrapper}>
      <EmojiPicker
        width={isMobile ? 250 : 375}
        height={300}
        onEmojiClick={onEmojiClick}
        lazyLoadEmojis={true}
        previewConfig={{
          showPreview: false,
          defaultCaption: "Your selected emoji",
          defaultEmoji: "👀",
        }}
        theme={
          isDarkMode
            ? ("dark" as Theme | undefined)
            : ("light" as Theme | undefined)
        }
      />
    </div>
  );
};

export default EmojiSelector;
