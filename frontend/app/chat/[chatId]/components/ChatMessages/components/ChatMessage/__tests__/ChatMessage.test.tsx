import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ChatMessage } from "../components/ChatMessage";

describe("ChatMessage", () => {
  it("should render chat messages with correct speaker and text", () => {
    const speaker = "user";
    const text = "Test user message";
    const { getByTestId } = render(
      <ChatMessage speaker={speaker} text={text} />
    );

    expect(getByTestId("chat-message-speaker")).toBeDefined();
    expect(getByTestId("chat-message-text")).toBeDefined();
  });
});
