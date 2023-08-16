// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
import { useFeature } from "@growthbook/growthbook-react";
import { $getRoot, EditorState } from "lexical";
import { useCallback, useEffect, useRef, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { getDebugTextContent } from "../helpers/getDebugTextContent";
import { queryMentions, Trigger } from "../helpers/queryMentions";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatBar = () => {
  const comboboxAnchor = useRef<HTMLDivElement>(null);
  const [menuOrComboboxOpen, setMenuOrComboboxOpen] = useState(false);
  const [comboboxItemSelected, setComboboxItemSelected] = useState(false);
  const [value, setValue] = useState<string>();

  const { allBrains } = useBrainContext();

  const [mentionItems, setMentionItems] = useState<Record<Trigger, string[]>>({
    "@": allBrains.map((brain) => brain.name),
  });

  useEffect(() => {
    setMentionItems({
      ...mentionItems,
      "@": allBrains.map((brain) => brain.name),
    });
  }, [allBrains]);

  const shouldUseNewUX = useFeature("new-ux").on;

  const handleChange = useCallback((editorState: EditorState) => {
    editorState.read(() => {
      const root = $getRoot();
      const content = getDebugTextContent(root);
      setValue(content);
    });
  }, []);

  const handleSearch = (trigger: string, queryString?: string | null) =>
    queryMentions(trigger, queryString, mentionItems);

  const handleMenuOrComboboxOpen = useCallback(() => {
    setMenuOrComboboxOpen(true);
  }, []);

  const handleMenuOrComboboxClose = useCallback(() => {
    setMenuOrComboboxOpen(false);
  }, []);

  const handleComboboxItemSelect = useCallback((label: string | null) => {
    setComboboxItemSelected(label !== null);
  }, []);

  return {
    comboboxAnchor,
    menuOrComboboxOpen,
    $getRoot,
    value,
    handleChange,
    handleSearch,
    handleMenuOrComboboxOpen,
    handleMenuOrComboboxClose,
    handleComboboxItemSelect,
    comboboxItemSelected,
    mentionItems,
  };
};
