import { useContext } from "react";

import { NotesEditorContext } from "../Notes-Editor-Provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useNotesEditorContext = () => {
  const context = useContext(NotesEditorContext);
  if (context === undefined) {
    throw new Error("useMenuContext must be used within a MenuProvider");
  }

  return context;
};
