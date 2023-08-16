/* eslint-disable max-lines */
"use client"; // prettier-ignore
import { sanitize } from "dompurify";
import { BeautifulMentionsPluginProps } from "lexical-beautiful-mentions";
import { createContext, PropsWithChildren, useCallback, useState } from "react";

import { useQueryParams } from "./hooks/useQueryParams";

interface Configuration
  extends Pick<BeautifulMentionsPluginProps, "allowSpaces" | "insertOnBlur"> {
  initialValue: string;
  autoFocus: "rootStart" | "rootEnd";
  asynchronous: boolean;
  commandFocus: boolean;
  combobox: boolean;
  mentionEnclosure?: string;
  showMentionsOnDelete: boolean;
  setAllowSpaces: (allowSpaces: boolean) => void;
  setInsertOnBlur: (insertOnBlur: boolean) => void;
  setMentionEnclosure: (mentionEnclosure: boolean) => void;
  setAsynchronous: (asynchronous: boolean) => void;
  setCombobox: (combobox: boolean) => void;
  setShowMentionsOnDelete: (showMentionsOnDelete: boolean) => void;
}

export const ConfigurationContext = createContext<Configuration | undefined>(
  undefined
);

export const ConfigurationProvider = ({
  children,
}: PropsWithChildren): JSX.Element => {
  const { updateQueryParam, hasQueryParams, getQueryParam } = useQueryParams();
  const [asynchronous, _setAsynchronous] = useState(
    getQueryParam("async") === "true"
  );
  const [allowSpaces, _setAllowSpaces] = useState(
    getQueryParam("space") === "true"
  );
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
  const initialValue = sanitize(valueParam) || (hasValue ?? "");
  const autoFocus: "rootStart" | "rootEnd" | "none" =
    focusParam === "start" ? "rootStart" : "rootEnd";

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

  const setInsertOnBlur = useCallback(
    (insertOnBlur: boolean) => {
      _setInsertOnBlur(insertOnBlur);
      updateQueryParam("blur", insertOnBlur);
    },
    [updateQueryParam]
  );

  return (
    <ConfigurationContext.Provider
      value={{
        initialValue,
        autoFocus,
        asynchronous,
        combobox,
        mentionEnclosure: mentionEnclosure ? '"' : undefined,
        showMentionsOnDelete,
        allowSpaces,
        insertOnBlur,
        setAsynchronous,
        setAllowSpaces,
        setInsertOnBlur,
        setCombobox,
        setMentionEnclosure,
        setShowMentionsOnDelete,
        commandFocus,
      }}
    >
      {children}
    </ConfigurationContext.Provider>
  );
};
