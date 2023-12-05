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
        messages: [],
        setMessages: () => void 0,
        updateStreamingHistory: () => void 0,
        notifications: [],
        setNotifications: () => void 0,
        removeMessage: () => void 0,
        sharedChatItems:[],
        setIsLoadingHistoryChatItems:() => void 0,
        isLoadingHistoryChatItems:false,
      }}
    >
      {children}
    </ChatContextMock.Provider>
  );
};
