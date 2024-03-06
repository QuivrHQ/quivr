"use client";

import { createContext, useState } from "react";

import { ThreadEntity } from "@/app/thread/[threadId]/types";

type ThreadsContextType = {
  allThreads: ThreadEntity[];
  //set setAllThreads is from the useState hook so it can take a function as params
  setAllThreads: React.Dispatch<React.SetStateAction<ThreadEntity[]>>;
  isLoading: boolean;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
};

export const ThreadsContext = createContext<ThreadsContextType | undefined>(
  undefined
);

export const ThreadsProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const [allThreads, setAllThreads] = useState<ThreadEntity[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  return (
    <ThreadsContext.Provider
      value={{
        allThreads,
        setAllThreads,
        isLoading,
        setIsLoading,
      }}
    >
      {children}
    </ThreadsContext.Provider>
  );
};
