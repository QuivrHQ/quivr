/* eslint-disable max-lines */
import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { MessagesDialog } from "../index";

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => ({
    session: {
      user: {},
    },
  }),
}));

vi.mock("../hooks/useMessagesDialog", () => ({
  useMessagesDialog: vi.fn(() => ({
    chatListRef: vi.fn(),
  })),
}));

const mockedUseChatContext = vi.fn(() => ({
  messages: [
    {
      assistant: "Test assistant message",
      message_id: "123",
      user_message: "Test user message",
      prompt_title: "Test prompt name",
      brain_name: "Test brain name",
    },
  ],
  notifications: [],
}));

vi.mock("@/lib/context", async () => {
  const actual = await vi.importActual<typeof import("@/lib/context")>(
    "@/lib/context"
  );

  return {
    ...actual,
    useChatContext: vi.fn().mockImplementation(() => mockedUseChatContext()),
  };
});

describe("ChatMessages", () => {
  it("should render chat messages correctly", () => {
    const { getAllByTestId } = render(<MessagesDialog />);
    expect(getAllByTestId("brain-tags")).toBeDefined();
    expect(getAllByTestId("prompt-tags")).toBeDefined();
    expect(getAllByTestId("chat-message-text")).toBeDefined();
  });

  it("should render placeholder text when history is empty", () => {
    mockedUseChatContext.mockImplementation(() => ({
      messages: [],
      notifications: [],
    }));

    const { getByTestId } = render(<MessagesDialog />);

    expect(getByTestId("empty-history-message")).toBeDefined();
  });
});
