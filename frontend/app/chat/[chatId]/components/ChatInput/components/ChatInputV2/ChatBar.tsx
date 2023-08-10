"use client";
import { AutoFocusPlugin } from "@lexical/react/LexicalAutoFocusPlugin";
import { LexicalComposer } from "@lexical/react/LexicalComposer";
import { ContentEditable } from "@lexical/react/LexicalContentEditable";
import LexicalErrorBoundary from "@lexical/react/LexicalErrorBoundary";
import { HistoryPlugin } from "@lexical/react/LexicalHistoryPlugin";
import { OnChangePlugin } from "@lexical/react/LexicalOnChangePlugin";
import { PlainTextPlugin } from "@lexical/react/LexicalPlainTextPlugin";
import { $getRoot } from "lexical";
import {
  BeautifulMentionsMenuItemProps,
  BeautifulMentionsMenuProps,
  BeautifulMentionsPlugin,
  ZeroWidthPlugin,
} from "lexical-beautiful-mentions";
import { forwardRef, useCallback, useRef, useState } from "react";

import Button from "@/lib/components/ui/Button";
import { cn } from "@/lib/utils";

import { useConfiguration } from "./ConfigurationProvider";
import { editorConfig } from "./editorConfig";
import { getDebugTextContent } from "./getDebugTextContent";

const MenuItem = forwardRef<HTMLLIElement, BeautifulMentionsMenuItemProps>(
  ({ selected, itemValue, label, ...props }, ref) => (
    <li
      ref={ref}
      className={cn(
        "m-0 flex min-w-[150px] shrink-0 cursor-pointer flex-row content-center whitespace-nowrap border-0 px-2.5 py-2 leading-4 text-slate-950 outline-none first:mt-1.5 last:mb-1.5 dark:text-slate-300",
        selected ? "bg-gray-100 dark:bg-gray-700" : "bg-white dark:bg-gray-900"
      )}
      {...props}
    >
      <div>
        {label}
        <Button
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            alert("delete");
          }}
        >
          Delete
        </Button>
      </div>
    </li>
  )
);

const Menu = forwardRef<any, BeautifulMentionsMenuProps>(
  ({ open, loading, ...other }, ref) => {
    if (loading) {
      return (
        <div
          ref={ref}
          className="mt-6 whitespace-nowrap rounded-lg bg-white p-2.5 text-slate-950 shadow-lg shadow-gray-900 dark:bg-gray-900 dark:text-slate-300"
        >
          Loading...
        </div>
      );
    }

    return (
      <ul
        ref={ref}
        style={{
          scrollbarWidth: "none",
          msOverflowStyle: "none",
        }}
        className="m-0 mt-6 list-none overflow-scroll overflow-y-scroll rounded-lg bg-white p-0 shadow-lg shadow-gray-900 dark:bg-gray-900"
        {...other}
      />
    );
  }
);

export default Menu;

const mentionItems = {
  "@": ["Anton", "Boris", "Catherine", "Dmitri", "Elena", "Felix", "Gina"],
};

const Placeholder = () => {
  const { combobox } = useConfiguration();

  return (
    <div
      className={cn(
        "pointer-events-none absolute inline-block select-none overflow-hidden overflow-ellipsis text-gray-500 dark:text-gray-400",
        combobox && "left-[14px] top-[18px]",
        !combobox && "left-3 top-4"
      )}
    >
      Enter some plain text...
    </div>
  );
};

const queryMentions = async (
  trigger: string,
  queryString: string,
  asynchronous: boolean
) => {
  const items = mentionItems[trigger];
  if (!items) {
    return [];
  }
  if (asynchronous) {
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  return items.filter((item) => {
    const value = typeof item === "string" ? item : item.value;

    return value.toLowerCase().includes(queryString.toLowerCase());
  });
};

export const ChatBar = (): JSX.Element => {
  const comboboxAnchor = useRef<HTMLDivElement>(null);
  const [menuOrComboboxOpen, setMenuOrComboboxOpen] = useState(false);
  const [comboboxItemSelected, setComboboxItemSelected] = useState(false);
  const [value, setValue] = useState<string>();

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

  const handleSearch = useCallback(
    (trigger: string, queryString: string) =>
      queryMentions(trigger, queryString, asynchronous),
    [asynchronous]
  );

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
      hello
      <LexicalComposer
        initialConfig={editorConfig(Object.keys(mentionItems), initialValue)}
      >
        hello
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
