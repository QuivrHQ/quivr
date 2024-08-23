import { useEffect, useRef, useState } from "react";

import { Tab } from "@/lib/types/Tab";

import styles from "./BrainSnippet.module.scss";

import { ColorSelector } from "../ui/ColorSelector/ColorSelector";
import EmojiSelector from "../ui/EmojiSelector/EmojiSelector";
import { QuivrButton } from "../ui/QuivrButton/QuivrButton";
import { Tabs } from "../ui/Tabs/Tabs";

export const BrainSnippet = ({
  setVisible,
  initialColor,
  initialEmoji,
  onSave,
}: {
  setVisible: React.Dispatch<React.SetStateAction<boolean>>;
  initialColor?: string;
  initialEmoji?: string;
  onSave: (color: string, emoji: string) => Promise<void> | void;
}): JSX.Element => {
  const [color, setColor] = useState(initialColor);
  const [emoji, setEmoji] = useState(initialEmoji);
  const [selectedTab, setSelectedTab] = useState("Emoji");

  const wrapperRef = useRef<HTMLDivElement>(null);

  const tabs: Tab[] = [
    {
      label: "Emoji",
      isSelected: selectedTab === "Emoji",
      onClick: () => setSelectedTab("Emoji"),
      iconName: "emoji",
    },
    {
      label: "Background",
      isSelected: selectedTab === "Colors",
      onClick: () => setSelectedTab("Colors"),
      iconName: "color",
    },
  ];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        wrapperRef.current &&
        !wrapperRef.current.contains(event.target as Node)
      ) {
        setVisible(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [setVisible]);

  return (
    <div ref={wrapperRef} className={styles.brain_snippet_wrapper}>
      <div className={styles.sample_wrapper} style={{ backgroundColor: color }}>
        <span>{emoji}</span>
      </div>
      <div className={styles.selector_wrapper}>
        <div className={styles.tabs}>
          <Tabs tabList={tabs} />
        </div>
        {selectedTab === "Emoji" && <EmojiSelector onSelectEmoji={setEmoji} />}
        {selectedTab === "Colors" && (
          <ColorSelector onSelectColor={setColor} color={color ?? ""} />
        )}
      </div>
      <div className={styles.button}>
        <QuivrButton
          label="Save"
          onClick={async () => {
            setVisible(false);
            await onSave(color ?? "", emoji ?? "");
          }}
          iconName="upload"
          color="primary"
        />
      </div>
    </div>
  );
};
