import { createContext, PropsWithChildren } from "react";

import { ChatContextProps } from "../types";

export const ChatContextMock = createContext<ChatContextProps | undefined>(
  undefined
);

export const ChatProviderMock = ({
  children,
}: PropsWithChildren): JSX.Element => {
  return (
    <ChatContextMock.Provider
      value={{
        history: [],
        setHistory: () => void 0,
        addToHistory: () => void 0,
        updateHistory: () => void 0,
        updateStreamingHistory: () => void 0,
      }}
    >
      {children}
    </ChatContextMock.Provider>
  );
};
