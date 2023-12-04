import { Editor } from "@tiptap/core";
import { useCallback, useEffect } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { getChatInputAttributesFromEditorState } from "../utils/getChatInputAttributesFromEditorState";

type UseEditorStateUpdaterProps = {
  editor: Editor | null;
  message: string;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useEditorStateUpdater = ({
  message,
  editor,
}: UseEditorStateUpdaterProps) => {
  const { currentBrain, currentPrompt } = useBrainContext();

  const setCurrentBrainAndPrompt = useCallback(() => {
    const { promptId, brainId } = getChatInputAttributesFromEditorState(editor);

    if (
      currentBrain !== undefined &&
      currentBrain.id !== brainId &&
      brainId === ""
    ) {
      editor
        ?.chain()
        .focus()
        .insertContent({
          type: "mention@",
          attrs: {
            id: currentBrain.id,
            label: currentBrain.name,
          },
        })
        .insertContent({
          type: "text",
          text: " ",
        })
        .run();
    }

    if (
      currentPrompt !== undefined &&
      currentPrompt.id !== promptId &&
      promptId === ""
    ) {
      editor
        ?.chain()
        .focus()
        .insertContent({
          type: "mention#",
          attrs: {
            id: currentPrompt.id,
            label: currentPrompt.title,
          },
        })
        .insertContent({
          type: "text",
          text: " ",
        })
        .run();
    }
  }, [currentBrain, currentPrompt, editor]);

  useEffect(() => {
    setCurrentBrainAndPrompt();
  }, [setCurrentBrainAndPrompt]);

  useEffect(() => {
    const { text } = getChatInputAttributesFromEditorState(editor);
    if (text !== message) {
      editor?.commands.setContent(message);
    }
    setCurrentBrainAndPrompt();
  }, [editor, message, setCurrentBrainAndPrompt]);
};
