import { useContext } from "react";

import { ChatContext } from "../ChatProvider";
import { ChatContextProps } from "../types";

export const useChatContext = (): ChatContextProps => {
  const context = useContext(ChatContext);

  if (context === undefined) {
    throw new Error("useChatContext must be used inside ChatProvider");
  }

  return context;
};
