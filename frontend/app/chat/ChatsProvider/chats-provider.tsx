"use client";

import { createContext } from "react";
import useChats from "./hooks/useChats";
import { ChatsState } from "./types";

export const ChatsContext = createContext<ChatsState | undefined>(undefined);

export const ChatsProvider = ({ children }: { children: React.ReactNode }) => {
  const chatsState = useChats();

  return (
    <ChatsContext.Provider value={chatsState}>{children}</ChatsContext.Provider>
  );
};
