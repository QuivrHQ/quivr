/* eslint-disable max-lines */
"use client";
import { AutoFocusPlugin } from "@lexical/react/LexicalAutoFocusPlugin";
import { LexicalComposer } from "@lexical/react/LexicalComposer";
import { ContentEditable } from "@lexical/react/LexicalContentEditable";
import LexicalErrorBoundary from "@lexical/react/LexicalErrorBoundary";
import { HistoryPlugin } from "@lexical/react/LexicalHistoryPlugin";
import { OnChangePlugin } from "@lexical/react/LexicalOnChangePlugin";
import { PlainTextPlugin } from "@lexical/react/LexicalPlainTextPlugin";
import {
  BeautifulMentionsPlugin,
  ZeroWidthPlugin,
} from "lexical-beautiful-mentions";

import { cn } from "@/lib/utils";

import { Menu } from "./components/Menu";
import { MenuItem } from "./components/MenuItem";
import { Placeholder } from "./components/Placeholder";
import { useConfiguration } from "./helpers/ConfigurationProvider/hooks/useConfiguration";
import { editorConfig } from "./helpers/editorConfig";
import { useChatBar } from "./hooks/useChatBar";

export const ChatBar = (): JSX.Element => {
  const {
    initialValue,
    autoFocus,
    allowSpaces,
    asynchronous,
    mentionEnclosure,
    insertOnBlur,
    showMentionsOnDelete,
  } = useConfiguration();

  const {
    handleChange,
    handleMenuOrComboboxClose,
    handleMenuOrComboboxOpen,
    handleSearch,
    mentionItems,
  } = useChatBar();

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
        <BeautifulMentionsPlugin
          onSearch={handleSearch}
          searchDelay={asynchronous ? 250 : 0}
          triggers={Object.keys(mentionItems)}
          mentionEnclosure={mentionEnclosure}
          allowSpaces={allowSpaces}
          insertOnBlur={insertOnBlur}
          showMentionsOnDelete={showMentionsOnDelete}
          menuComponent={Menu}
          menuItemComponent={MenuItem}
          onMenuOpen={handleMenuOrComboboxOpen}
          onMenuClose={handleMenuOrComboboxClose}
        />

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
        <AutoFocusPlugin defaultSelection={autoFocus} />
        <ZeroWidthPlugin />
      </LexicalComposer>
    </div>
  );
};
