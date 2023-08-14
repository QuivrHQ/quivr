/* eslint-disable max-lines */
"use client";
import { useFeature } from "@growthbook/growthbook-react";
import { AutoFocusPlugin } from "@lexical/react/LexicalAutoFocusPlugin";
import { LexicalComposer } from "@lexical/react/LexicalComposer";
import { ContentEditable } from "@lexical/react/LexicalContentEditable";
import LexicalErrorBoundary from "@lexical/react/LexicalErrorBoundary";
import { HistoryPlugin } from "@lexical/react/LexicalHistoryPlugin";
import { OnChangePlugin } from "@lexical/react/LexicalOnChangePlugin";
import { PlainTextPlugin } from "@lexical/react/LexicalPlainTextPlugin";
import { $getRoot, EditorState } from "lexical";
import {
  BeautifulMentionsPlugin,
  ZeroWidthPlugin,
} from "lexical-beautiful-mentions";
import { useCallback, useRef, useState } from "react";

import { cn } from "@/lib/utils";

import { useConfiguration } from "./ConfigurationProvider/hooks/useConfiguration";
import { Placeholder } from "./components/Placeholder";
import { editorConfig } from "./editorConfig";
import { getDebugTextContent } from "./getDebugTextContent";
import { Trigger, mentionItems, queryMentions } from "./helpers/queryMentions";

export const ChatBar = (): JSX.Element => {
  const comboboxAnchor = useRef<HTMLDivElement>(null);
  const [menuOrComboboxOpen, setMenuOrComboboxOpen] = useState(false);
  const [comboboxItemSelected, setComboboxItemSelected] = useState(false);
  const [value, setValue] = useState<string>();

  const shouldUseNewUX = useFeature("new-ux").on;

  const {
    asynchronous,
    autoFocus,
    allowSpaces,
    creatable,
    insertOnBlur,
    combobox,
    mentionEnclosure,
    showMentionsOnDelete,
  } = useConfiguration();

  const handleChange = useCallback((editorState: EditorState) => {
    editorState.read(() => {
      const root = $getRoot();
      const content = getDebugTextContent(root);
      setValue(content);
    });
  }, []);

  const handleSearch = (trigger: Trigger, queryString: string) =>
    queryMentions(trigger, queryString);

  const handleMenuOrComboboxOpen = useCallback(() => {
    setMenuOrComboboxOpen(true);
  }, []);

  const handleMenuOrComboboxClose = useCallback(() => {
    setMenuOrComboboxOpen(false);
  }, []);

  const handleComboboxItemSelect = useCallback((label: string | null) => {
    setComboboxItemSelected(label !== null);
  }, []);
  const { initialValue } = useConfiguration();

  return (
    <div
      className="mt-5 w-full max-w-2xl"
      style={{
        borderWidth: 1,
        borderColor: "black",
        borderStyle: "solid",
        flex: 1,
      }}
    >
      <LexicalComposer
        initialConfig={editorConfig(Object.keys(mentionItems), initialValue)}
      >
        {!combobox && (
          <BeautifulMentionsPlugin
            onSearch={handleSearch}
            searchDelay={asynchronous ? 250 : 0}
            triggers={Object.keys(mentionItems)}
            mentionEnclosure={mentionEnclosure}
            allowSpaces={allowSpaces}
            creatable={creatable}
            insertOnBlur={insertOnBlur}
            showMentionsOnDelete={showMentionsOnDelete}
            menuComponent={Menu}
            menuItemComponent={MenuItem}
            onMenuOpen={handleMenuOrComboboxOpen}
            onMenuClose={handleMenuOrComboboxClose}
          />
        )}
        {combobox && (
          <BeautifulMentionsPlugin
            onSearch={handleSearch}
            searchDelay={asynchronous ? 250 : 0}
            triggers={Object.keys(mentionItems)}
            mentionEnclosure={mentionEnclosure}
            allowSpaces={allowSpaces}
            creatable={creatable}
            showMentionsOnDelete={showMentionsOnDelete}
            combobox
            comboboxAnchor={comboboxAnchor.current}
            comboboxAnchorClassName="shadow-lg shadow-gray-900 rounded"
            comboboxComponent={Combobox}
            comboboxItemComponent={ComboboxItem}
            onComboboxOpen={handleMenuOrComboboxOpen}
            onComboboxClose={handleMenuOrComboboxClose}
            onComboboxFocusChange={handleComboboxItemSelect}
          />
        )}
        <PlainTextPlugin
          contentEditable={
            <ContentEditable
              style={{ tabSize: 1 }}
              className={cn(
                "relative resize-none caret-gray-900 outline-none outline-0 dark:text-gray-100 dark:caret-gray-100"
              )}
            />
          }
          placeholder={<Placeholder />}
          ErrorBoundary={LexicalErrorBoundary}
        />
        <OnChangePlugin onChange={handleChange} />
        <HistoryPlugin />
        {autoFocus !== "none" && (
          <AutoFocusPlugin defaultSelection={autoFocus} />
        )}
        <ZeroWidthPlugin />
      </LexicalComposer>
    </div>
  );
};
