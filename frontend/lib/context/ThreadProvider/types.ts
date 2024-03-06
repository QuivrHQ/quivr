import { Notification, ThreadMessage } from "@/app/thread/[threadId]/types";

import { Model } from "../../types/BrainConfig";

export type ThreadConfig = {
  model: Model;
  temperature: number;
  maxTokens: number;
};

export type ThreadContextProps = {
  messages: ThreadMessage[];
  setMessages: (history: ThreadMessage[]) => void;
  updateStreamingHistory: (streamedThread: ThreadMessage) => void;
  notifications: Notification[];
  setNotifications: (notifications: Notification[]) => void;
  removeMessage: (id: string) => void;
  sourcesMessageIndex: number | undefined;
  setSourcesMessageIndex: (index: number | undefined) => void;
};
