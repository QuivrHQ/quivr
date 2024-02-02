import { Editor, EditorEvents } from "@tiptap/core";
import { UUID } from "crypto";
import { useCallback, useEffect } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { getChatInputAttributesFromEditorState } from "../utils/getChatInputAttributesFromEditorState";
import { removeExistingMentionFromEditor } from "../utils/removeExistingMentionFromEditor";

type UseChatStateUpdaterProps = {
  editor: Editor | null;
  setMessage: (message: string) => void;
};
// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatStateUpdater = ({
  editor,
  setMessage,
}: UseChatStateUpdaterProps) => {
  const {
    currentBrainId,
    currentPromptId,
    setCurrentBrainId,
    setCurrentPromptId,
  } = useBrainContext();

  const onEditorUpdate = useCallback(
    ({ editor: editorNewState }: EditorEvents["update"]) => {
      const { text, brainId, promptId } =
        getChatInputAttributesFromEditorState(editorNewState);

      setMessage(text);

      if (brainId !== currentBrainId) {
        if (brainId === "") {
          return;
        } else {
          if (currentBrainId !== null) {
            removeExistingMentionFromEditor(editorNewState, "mention@");
          }
          setCurrentBrainId(brainId as UUID);
        }
      }
      if (promptId !== currentPromptId) {
        if (promptId === "") {
          setCurrentPromptId(null);
        } else {
          if (currentPromptId !== null) {
            removeExistingMentionFromEditor(editorNewState, "mention#");
          }
          setCurrentPromptId(promptId as UUID);
        }
      }
    },
    [
      currentBrainId,
      currentPromptId,
      setCurrentBrainId,
      setCurrentPromptId,
      setMessage,
    ]
  );

  useEffect(() => {
    editor?.on("update", onEditorUpdate);

    return () => {
      editor?.off("update", onEditorUpdate);
    };
  }, [editor, onEditorUpdate, setMessage]);
};
