import React, { createContext, useState } from "react";

type NotesEditorContextType = {
  content: string;
  updateContent: (newContent: string) => void;
};

export const NotesEditorContext = createContext<
  NotesEditorContextType | undefined
>(undefined);

export const NotesEditorProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [content, setContent] = useState("");

  const updateContent = (newContent: string) => {
    setContent(newContent);
  };

  return (
    <NotesEditorContext.Provider value={{ content, updateContent }}>
      {children}
    </NotesEditorContext.Provider>
  );
};
