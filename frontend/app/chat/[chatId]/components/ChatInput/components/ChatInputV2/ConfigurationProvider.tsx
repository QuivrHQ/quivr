"use client"; // prettier-ignore
import { sanitize } from "dompurify";
import { BeautifulMentionsPluginProps } from "lexical-beautiful-mentions";
import {
  createContext,
  PropsWithChildren,
  useCallback,
  useContext,
  useState,
} from "react";

import { defaultInitialValue } from "./editorConfig";
import { useQueryParams } from "./useQueryParams";

interface Configuration
  extends Pick<
    BeautifulMentionsPluginProps,
    "allowSpaces" | "creatable" | "insertOnBlur"
  > {
  initialValue: string;
  autoFocus: "rootStart" | "rootEnd" | "none";
  asynchronous: boolean;
  commandFocus: boolean;
  combobox: boolean;
  mentionEnclosure?: string;
  showMentionsOnDelete: boolean;
  setAllowSpaces: (allowSpaces: boolean) => void;
  setCreatable: (creatable: boolean) => void;
  setInsertOnBlur: (insertOnBlur: boolean) => void;
  setMentionEnclosure: (mentionEnclosure: boolean) => void;
  setAsynchronous: (asynchronous: boolean) => void;
  setCombobox: (combobox: boolean) => void;
  setShowMentionsOnDelete: (showMentionsOnDelete: boolean) => void;
}

const ConfigurationCtx = createContext<Configuration>(undefined);

const creatableMap = {
  "@": 'Add user "{{name}}"',
  "#": 'Add tag "{{name}}"',
  "due:": 'Add due date "{{name}}"',
  "rec:": 'Add recurrence "{{name}}"',
};

export const ConfigurationProvider = ({ children }: PropsWithChildren) => {
  const { updateQueryParam, hasQueryParams, getQueryParam } = useQueryParams();
  const [asynchronous, _setAsynchronous] = useState(
    getQueryParam("async") === "true"
  );
  const [allowSpaces, _setAllowSpaces] = useState(
    getQueryParam("space") === "true"
  );
  const [creatable, _setCreatable] = useState(getQueryParam("new") === "true");
  const [insertOnBlur, _setInsertOnBlur] = useState(
    getQueryParam("blur") === "true"
  );
  const [combobox, _setCombobox] = useState(
    getQueryParam("combobox") === "true"
  );
  const [mentionEnclosure, _setMentionEnclosure] = useState(
    getQueryParam("enclosure") === "true"
  );
  const [showMentionsOnDelete, _setShowMentionsOnDelete] = useState(
    getQueryParam("mentions") === "true"
  );
  const commandFocus = getQueryParam("cf") !== "false";
  const focusParam = getQueryParam("focus");
  const valueParam = getQueryParam("value");
  const hasValue = hasQueryParams("value");
  const initialValue =
    sanitize(valueParam) || (hasValue ? "" : defaultInitialValue);
  const autoFocus: "rootStart" | "rootEnd" | "none" =
    focusParam === "start"
      ? "rootStart"
      : focusParam === "none"
      ? "none"
      : "rootEnd";

  const setAsynchronous = useCallback(
    (asynchronous: boolean) => {
      _setAsynchronous(asynchronous);
      updateQueryParam("async", asynchronous);
    },
    [updateQueryParam]
  );

  const setCombobox = useCallback(
    (combobox: boolean) => {
      _setCombobox(combobox);
      updateQueryParam("combobox", combobox);
    },
    [updateQueryParam]
  );

  const setMentionEnclosure = useCallback(
    (mentionEnclosure: boolean) => {
      _setMentionEnclosure(mentionEnclosure);
      updateQueryParam("enclosure", mentionEnclosure);
    },
    [updateQueryParam]
  );

  const setShowMentionsOnDelete = useCallback(
    (showMentionsOnDelete: boolean) => {
      _setShowMentionsOnDelete(showMentionsOnDelete);
      updateQueryParam("mentions", showMentionsOnDelete);
    },
    [updateQueryParam]
  );

  const setAllowSpaces = useCallback(
    (allowSpaces: boolean) => {
      _setAllowSpaces(allowSpaces);
      updateQueryParam("space", allowSpaces);
    },
    [updateQueryParam]
  );

  const setCreatable = useCallback(
    (creatable: boolean) => {
      _setCreatable(creatable);
      updateQueryParam("new", creatable);
    },
    [updateQueryParam]
  );

  const setInsertOnBlur = useCallback(
    (insertOnBlur: boolean) => {
      _setInsertOnBlur(insertOnBlur);
      updateQueryParam("blur", insertOnBlur);
    },
    [updateQueryParam]
  );

  return (
    <ConfigurationCtx.Provider
      value={{
        initialValue,
        autoFocus,
        asynchronous,
        combobox,
        mentionEnclosure: mentionEnclosure ? '"' : undefined,
        showMentionsOnDelete,
        allowSpaces,
        creatable: creatable ? creatableMap : false,
        insertOnBlur,
        setAsynchronous,
        setAllowSpaces,
        setCreatable,
        setInsertOnBlur,
        setCombobox,
        setMentionEnclosure,
        setShowMentionsOnDelete,
        commandFocus,
      }}
    >
      {children}
    </ConfigurationCtx.Provider>
  );
};

export function useConfiguration() {
  const context = useContext(ConfigurationCtx);
  if (context === undefined) {
    throw new Error(
      "useConfiguration must be used within a ConfigurationProvider"
    );
  }

  return context;
}
