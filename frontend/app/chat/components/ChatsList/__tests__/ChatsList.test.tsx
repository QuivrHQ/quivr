/* eslint-disable max-lines */
import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  ChatContextMock,
  ChatProviderMock,
} from "@/lib/context/ChatProvider/mocks/ChatProviderMock";

import * as useChatsListModule from "../hooks/useChatsList";
import { ChatsList } from "../index";

const getChatsMock = vi.fn(() => []);

const setOpenMock = vi.fn();

vi.mock("next/navigation", async () => {
  const actual = await vi.importActual<typeof import("next/navigation")>(
    "next/navigation"
  );

  return { ...actual, useRouter: () => ({ replace: vi.fn() }) };
});

vi.mock("@/lib/context/ChatsProvider/hooks/useChatsContext", () => ({
  useChatsContext: () => ({
    allChats: [
      { chat_id: 1, name: "Chat 1" },
      { chat_id: 2, name: "Chat 2" },
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

describe("ChatsList", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should render correctly", () => {
    const { getByTestId } = render(
      <ChatProviderMock>
        <ChatsList />
      </ChatProviderMock>
    );
    const chatsList = getByTestId("chats-list");
    expect(chatsList).toBeDefined();

    const newChatButton = getByTestId("new-chat-button");
    expect(newChatButton).toBeDefined();

    const toggleButton = getByTestId("chats-list-toggle");
    expect(toggleButton).toBeDefined();
  });

  it("renders the chats list with correct number of items", () => {
    render(
      <ChatProviderMock>
        <ChatsList />
      </ChatProviderMock>
    );
    const chatItems = screen.getAllByTestId("chats-list-item");
    expect(chatItems).toHaveLength(2);
  });

  it("toggles the open state when the button is clicked", async () => {
    vi.spyOn(useChatsListModule, "useChatsList").mockReturnValue({
      open: false,
      setOpen: setOpenMock,
    });

    await act(() =>
      render(
        <ChatProviderMock>
          (<ChatsList />)
        </ChatProviderMock>
      )
    );

    const toggleButton = screen.getByTestId("chats-list-toggle");

    fireEvent.click(toggleButton);

    expect(setOpenMock).toHaveBeenCalledTimes(1);
  });

  it("should call getChats when the component mounts", async () => {
    vi.mock("@/lib/api/chat/useChatApi", () => ({
      useChatApi: () => ({
        getChats: () => getChatsMock(),
      }),
    }));
    await act(() =>
      render(
        <ChatProviderMock>
          <ChatsList />
        </ChatProviderMock>
      )
    );

    expect(getChatsMock).toHaveBeenCalledTimes(1);
  });
});
