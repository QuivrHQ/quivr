/* eslint-disable max-lines */
import { MentionData } from "@draft-js-plugins/mention";
import { EditorState } from "draft-js";
import { useEffect, useMemo, useState } from "react";

import { requiredRolesForUpload } from "@/app/upload/config";
import { mapMinimalBrainToMentionData } from "@/lib/components/MentionInput";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { MentionInputMentionsType } from "../../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionState = () => {
  const { allBrains } = useBrainContext();

  const brainsWithUploadRights = useMemo(
    () =>
      allBrains.filter((brain) => requiredRolesForUpload.includes(brain.role)),
    [allBrains]
  );

  const [editorState, setEditorState] = useState(EditorState.createEmpty());

  const [mentionItems, setMentionItems] = useState<MentionInputMentionsType>({
    "@": brainsWithUploadRights.map(mapMinimalBrainToMentionData),
  });

  const [suggestions, setSuggestions] = useState<MentionData[]>([]);

  useEffect(() => {
    setMentionItems({
      "@": brainsWithUploadRights.map(mapMinimalBrainToMentionData),
    });
  }, [brainsWithUploadRights]);

  return {
    editorState,
    setEditorState,
    mentionItems,
    setSuggestions,
    setMentionItems,
    suggestions,
  };
};
