import React, { createContext, useState } from "react";

type NotesEditorContextType = {
  content: string;
  updateContent: (newContent: string) => void;
  expand: boolean;
  setExpand: (expand: boolean) => void;
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
  const [expand, setExpand] = useState<boolean>(false);

  const updateContent = (newContent: string) => {
    setContent(newContent);
  };

  return (
    <NotesEditorContext.Provider
      value={{ content, updateContent, expand, setExpand }}
    >
      {children}
    </NotesEditorContext.Provider>
  );
};
