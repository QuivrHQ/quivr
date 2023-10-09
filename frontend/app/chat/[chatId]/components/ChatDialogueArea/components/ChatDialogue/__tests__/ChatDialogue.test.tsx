import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ChatMessage } from "@/app/chat/[chatId]/types";

import { ChatDialogue } from "..";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "../../../utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => ({
    session: {
      user: {},
    },
  }),
}));

vi.mock("../hooks/useChatDialogue", () => ({
  useChatDialogue: vi.fn(() => ({
    chatListRef: vi.fn(),
  })),
}));
const queryClient = new QueryClient();

describe("ChatDialogue", () => {
  it("should render chat messages correctly", () => {
    const messages: ChatMessage[] = [
      {
        assistant: "Test assistant message",
        message_id: "123",
        user_message: "Test user message",
        prompt_title: "Test prompt name",
        brain_name: "Test brain name",
        chat_id: "",
        message_time: "",
      },
    ];
    const chatItems = getMergedChatMessagesWithDoneStatusNotificationsReduced(
      messages,
      []
    );
    const { getAllByTestId } = render(
      <QueryClientProvider client={queryClient}>
        <ChatDialogue chatItems={chatItems} />
      </QueryClientProvider>
    );
    expect(getAllByTestId("brain-tags")).toBeDefined();
    expect(getAllByTestId("prompt-tags")).toBeDefined();
    expect(getAllByTestId("chat-message-text")).toBeDefined();
  });

  it("should render placeholder text when history is empty", () => {
    const { getByTestId } = render(
      <QueryClientProvider client={queryClient}>
        <ChatDialogue chatItems={[]} />
      </QueryClientProvider>
    );

    expect(getByTestId("empty-history-message")).toBeDefined();
  });
});
