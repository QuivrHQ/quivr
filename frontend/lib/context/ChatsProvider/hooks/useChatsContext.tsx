import { useContext } from "react";

import { ChatsContext } from "../chats-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatsContext = () => {
  const context = useContext(ChatsContext);

  if (context === undefined) {
    throw new Error("useChatsStore must be used inside ChatsProvider");
  }

  return context;
};
