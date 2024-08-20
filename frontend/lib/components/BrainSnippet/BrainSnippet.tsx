import { useState } from "react";

import { Tab } from "@/lib/types/Tab";

import styles from "./BrainSnippet.module.scss";

import { ColorSelector } from "../ui/ColorSelector/ColorSelector";
import EmojiSelector from "../ui/EmojiSelector/EmojiSelector";
import { Tabs } from "../ui/Tabs/Tabs";

export const BrainSnippet = (): JSX.Element => {
  const [color, setColor] = useState("#aabbcc");
  const [emoji, setEmoji] = useState("🧠");
  const [selectedTab, setSelectedTab] = useState("Emoji");

  const tabs: Tab[] = [
    {
      label: "",
      isSelected: selectedTab === "Emoji",
      onClick: () => setSelectedTab("Emoji"),
      iconName: "emoji",
    },
    {
      label: "",
      isSelected: selectedTab === "Colors",
      onClick: () => setSelectedTab("Colors"),
      iconName: "color",
    },
  ];

  return (
    <div className={styles.brain_snippet_wrapper}>
      <div className={styles.sample_wrapper} style={{ backgroundColor: color }}>
        <span>{emoji}</span>
      </div>
      <div className={styles.selector_wrapper}>
        <div className={styles.tabs}>
          <Tabs tabList={tabs} />
        </div>
        {selectedTab === "Emoji" && <EmojiSelector onSelectEmoji={setEmoji} />}
        {selectedTab === "Colors" && (
          <ColorSelector onSelectColor={setColor} color={color} />
        )}
      </div>
    </div>
  );
};
