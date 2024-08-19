import { Picker } from "emoji-mart";
import { SetStateAction, useState } from "react";

export const EmojiSelector = (): JSX.Element => {
  const [selectedEmoji, setSelectedEmoji] = useState(null);

  const addEmoji = (emoji: { native: SetStateAction<null> }) => {
    setSelectedEmoji(emoji.native);
  };

  return (
    <div>
      {selectedEmoji ? <span>{selectedEmoji}</span> : null}
      <Picker onSelect={addEmoji} />
    </div>
  );
};
