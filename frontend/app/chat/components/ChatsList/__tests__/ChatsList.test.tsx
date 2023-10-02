/* eslint-disable max-lines */
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  BrainContextMock,
  BrainProviderMock,
} from "@/lib/context/BrainProvider/mocks/BrainProviderMock";
import {
  ChatContextMock,
  ChatProviderMock,
} from "@/lib/context/ChatProvider/mocks/ChatProviderMock";
import { KnowledgeToFeedProvider } from "@/lib/context/KnowledgeToFeedProvider";
import { SupabaseContextMock } from "@/lib/context/SupabaseProvider/mocks/SupabaseProviderMock";

vi.mock("@/lib/context/SupabaseProvider/supabase-provider", () => ({
  SupabaseContext: SupabaseContextMock,
}));

import { ChatsList } from "../index";

const getChatsMock = vi.fn(() => []);
const queryClient = new QueryClient();

vi.mock("next/navigation", async () => {
  const actual = await vi.importActual<typeof import("next/navigation")>(
    "next/navigation"
  );

  return { ...actual, useRouter: () => ({ replace: vi.fn() }) };
});

vi.mock("@/lib/context/ChatsProvider/hooks/useChatsContext", () => ({
  useChatsContext: () => ({
    allChats: [
      {
        chat_id: 1,
        name: "Chat 1",
        creation_time: new Date().toISOString(),
      },
      {
        chat_id: 2,
        name: "Chat 2",
        creation_time: new Date().toISOString(),
      },
    ],

    deleteChat: vi.fn(),
    setAllChats: vi.fn(),
  }),
}));

vi.mock("@/lib/hooks", async () => {
  const actual = await vi.importActual<typeof import("@/lib/hooks")>(
    "@/lib/hooks"
  );

  return {
    ...actual,
    useAxios: () => ({
      axiosInstance: vi.fn(),
    }),
  };
});
vi.mock("@/lib/context/ChatProvider/ChatProvider", () => ({
  ChatContext: ChatContextMock,
}));
vi.mock("@/lib/context/BrainProvider/brain-provider", () => ({
  BrainContext: BrainContextMock,
}));

const mockUseSupabase = vi.fn(() => ({
  session: {
    user: { email: "email@domain.com" },
  },
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

describe("ChatsList", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should render correctly", () => {
    const { getByTestId } = render(
      <QueryClientProvider client={queryClient}>
        <KnowledgeToFeedProvider>
          <ChatProviderMock>
            <BrainProviderMock>
              <ChatsList />
            </BrainProviderMock>
          </ChatProviderMock>
        </KnowledgeToFeedProvider>
      </QueryClientProvider>
    );
    const chatsList = getByTestId("chats-list");
    expect(chatsList).toBeDefined();

    const newChatButton = getByTestId("new-chat-button");
    expect(newChatButton).toBeDefined();
  });

  it("renders the chats list with correct number of items", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <KnowledgeToFeedProvider>
          <ChatProviderMock>
            <BrainProviderMock>
              <ChatsList />
            </BrainProviderMock>
          </ChatProviderMock>
        </KnowledgeToFeedProvider>
      </QueryClientProvider>
    );
    const chatItems = screen.getAllByTestId("chats-list-item");
    expect(chatItems).toHaveLength(2);
  });

  it("should call getChats when the component mounts", async () => {
    vi.mock("@/lib/api/chat/useChatApi", () => ({
      useChatApi: () => ({
        getChats: () => getChatsMock(),
      }),
    }));

    await act(() =>
      render(
        <QueryClientProvider client={queryClient}>
          <KnowledgeToFeedProvider>
            <ChatProviderMock>
              <BrainProviderMock>
                <ChatsList />
              </BrainProviderMock>
            </ChatProviderMock>
          </KnowledgeToFeedProvider>
        </QueryClientProvider>
      )
    );

    expect(getChatsMock).toHaveBeenCalledTimes(1);
  });
});
