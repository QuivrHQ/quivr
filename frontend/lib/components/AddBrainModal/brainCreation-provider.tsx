import { createContext, useContext, useState } from "react";

interface BrainCreationContextProps {
  isBrainCreationModalOpened: boolean;
  setIsBrainCreationModalOpened: React.Dispatch<React.SetStateAction<boolean>>;
  creating: boolean;
  setCreating: React.Dispatch<React.SetStateAction<boolean>>;
  snippetColor: string;
  setSnippetColor: React.Dispatch<React.SetStateAction<string>>;
  snippetEmoji: string;
  setSnippetEmoji: React.Dispatch<React.SetStateAction<string>>;
}

export const BrainCreationContext = createContext<
  BrainCreationContextProps | undefined
>(undefined);

export const BrainCreationProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [isBrainCreationModalOpened, setIsBrainCreationModalOpened] =
    useState<boolean>(false);
  const [creating, setCreating] = useState<boolean>(false);
  const [snippetColor, setSnippetColor] = useState<string>("#d0c6f2");
  const [snippetEmoji, setSnippetEmoji] = useState<string>("🧠");

  return (
    <BrainCreationContext.Provider
      value={{
        isBrainCreationModalOpened,
        setIsBrainCreationModalOpened,
        creating,
        setCreating,
        snippetColor,
        setSnippetColor,
        snippetEmoji,
        setSnippetEmoji,
      }}
    >
      {children}
    </BrainCreationContext.Provider>
  );
};

export const useBrainCreationContext = (): BrainCreationContextProps => {
  const context = useContext(BrainCreationContext);
  if (!context) {
    throw new Error(
      "useBrainCreationContext must be used within a BrainCreationProvider"
    );
  }

  return context;
};
