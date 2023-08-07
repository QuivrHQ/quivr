import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ChatMessages } from "../index";

// Mocking the useChatMessages hook
vi.mock("../hooks/useChatMessages", () => ({
  useChatMessages: vi.fn(() => ({
    chatListRef: {
      current: null,
    },
  })),
}));

const useChatContextMock = vi.fn(() => ({
  history: [
    {
      assistant: "Test assistant message",
      message_id: "123",
      user_message: "Test user message",
    },
  ],
}));

// Mocking the useChatContext hook
vi.mock("@/lib/context", () => ({
  useChatContext: () => useChatContextMock(),
}));

describe("ChatMessages", () => {
  it("should render chat messages correctly", () => {
    const { getAllByTestId } = render(<ChatMessages />);

    expect(getAllByTestId("chat-message-speaker")).toBeDefined();

    expect(getAllByTestId("chat-message-text")).toBeDefined();
  });

  it("should render placeholder text when history is empty", () => {
    // Mocking the useChatContext hook to return an empty history
    useChatContextMock.mockReturnValue({ history: [] });

    const { getByTestId } = render(<ChatMessages />);

    expect(getByTestId("empty-history-message")).toBeDefined();
  });
});
