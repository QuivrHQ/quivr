"use client";

import { createContext, useState } from "react";

import { ChatEntity } from "@/app/chat/[chatId]/types";

type ChatsContextType = {
  allChats: ChatEntity[];
  //set setAllChats is from the useState hook so it can take a function as params
  setAllChats: React.Dispatch<React.SetStateAction<ChatEntity[]>>;
  isLoading: boolean;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
};

export const ChatsContext = createContext<ChatsContextType | undefined>(
  undefined
);

export const ChatsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [allChats, setAllChats] = useState<ChatEntity[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  return (
    <ChatsContext.Provider
      value={{
        allChats,
        setAllChats,
        isLoading,
        setIsLoading,
      }}
    >
      {children}
    </ChatsContext.Provider>
  );
};
