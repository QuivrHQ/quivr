import { createContext, PropsWithChildren } from "react";

import { ThreadContextProps } from "../types";

export const ThreadContextMock = createContext<ThreadContextProps | undefined>(
  undefined
);

export const ThreadProviderMock = ({
  children,
}: PropsWithChildren): JSX.Element => {
  return (
    <ThreadContextMock.Provider
      value={{
        messages: [],
        setMessages: () => void 0,
        updateStreamingHistory: () => void 0,
        notifications: [],
        setNotifications: () => void 0,
        removeMessage: () => void 0,
        sourcesMessageIndex: undefined,
        setSourcesMessageIndex: () => void 0,
      }}
    >
      {children}
    </ThreadContextMock.Provider>
  );
};
