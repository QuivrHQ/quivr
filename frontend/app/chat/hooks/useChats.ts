import { useState } from "react";
import { Chat } from "../types";

export default function useChats() {
  const [chats, setChats] = useState<Chat[]>([]);

  return { chats, setChats };
}
