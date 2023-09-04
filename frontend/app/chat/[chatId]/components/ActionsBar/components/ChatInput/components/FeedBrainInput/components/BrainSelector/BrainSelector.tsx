import Editor from "@draft-js-plugins/editor";
import { ReactElement } from "react";
import { useTranslation } from "react-i18next";

import "@draft-js-plugins/mention/lib/plugin.css";
import "draft-js/dist/Draft.css";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainSuggestionsContainer } from "./components";
import { SuggestionRow } from "./components/SuggestionRow";
import { useBrainSelector } from "./hooks/useBrainSelector";

export const BrainSelector = (): ReactElement => {
  const {
    mentionInputRef,
    MentionSuggestions,
    keyBindingFn,
    editorState,
    onAddMention,
    setOpen,
    onSearchChange,
    open,
    plugins,
    suggestions,
    handleEditorChange,
  } = useBrainSelector();
  const { currentBrainId } = useBrainContext();

  const { t } = useTranslation(["chat"]);

  const hasBrainSelected = currentBrainId !== null;

  return (
    <div className="w-full" data-testid="chat-input">
      <Editor
        editorKey={"editor"}
        editorState={editorState}
        onChange={handleEditorChange}
        plugins={plugins}
        ref={mentionInputRef}
        placeholder={hasBrainSelected ? "" : t("feed_brain_placeholder")}
        keyBindingFn={keyBindingFn}
        readOnly={hasBrainSelected}
      />
      <div
        style={{
          // `open` should be directly passed to the MentionSuggestions component.
          // However, it is not working as expected since we are not able to click on button in custom suggestion renderer.
          // So, we are using this hack to make it work.
          opacity: open ? 1 : 0,
        }}
      >
        <MentionSuggestions
          open
          onOpenChange={setOpen}
          suggestions={suggestions}
          onSearchChange={onSearchChange}
          popoverContainer={BrainSuggestionsContainer}
          entryComponent={SuggestionRow}
          renderEmptyPopup
          onAddMention={onAddMention}
        />
      </div>
    </div>
  );
};
