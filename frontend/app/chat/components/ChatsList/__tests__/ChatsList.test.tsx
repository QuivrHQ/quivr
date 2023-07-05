import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ChatsList } from "../index";

const setOpenMock = vi.fn(() => ({}));

vi.mock("../hooks/useChatsList", () => ({
  useChatsList: () => ({
    open: false,
    setOpen: () => setOpenMock(),
  }),
}));

vi.mock("@/lib/context/ChatsProvider/hooks/useChatsContext", () => ({
  useChatsContext: () => ({
    allChats: [
      { chat_id: 1, name: "Chat 1" },
      { chat_id: 2, name: "Chat 2" },
    ],
    deleteChat: vi.fn(),
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

describe("ChatsList", () => {
  it("should render correctly", () => {
    const { getByTestId } = render(<ChatsList />);
    const chatsList = getByTestId("chats-list");
    expect(chatsList).toBeDefined();

    const newChatButton = getByTestId("new-chat-button");
    expect(newChatButton).toBeDefined();

    const toggleButton = getByTestId("chats-list-toggle");
    expect(toggleButton).toBeDefined();
  });

  it("renders the chats list with correct number of items", () => {
    render(<ChatsList />);
    const chatItems = screen.getAllByTestId("chats-list-item");
    expect(chatItems).toHaveLength(2);
  });

  it("toggles the open state when the button is clicked", () => {
    render(<ChatsList />);
    const toggleButton = screen.getByTestId("chats-list-toggle");
    fireEvent.click(toggleButton);

    expect(setOpenMock).toHaveBeenCalledTimes(1);
  });
});
