import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ChatMessage } from "../components/ChatMessage";

describe("ChatMessage", () => {
  it("should render chat messages with correct speaker and text", () => {
    const speaker = "user";
    const text = "Test user message";
    const { getByText } = render(<ChatMessage speaker={speaker} text={text} />);

    const speakerElement = getByText(speaker);
    const textElement = getByText(text);

    expect(speakerElement).toBeDefined();
    expect(textElement).toBeDefined();
  });
});
