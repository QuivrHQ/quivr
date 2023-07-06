import { fireEvent, render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ChatInput } from "../index";

const addQuestionMock = vi.fn((...params: unknown[]) => ({ params }));

vi.mock("@/app/chat/[chatId]/hooks/useChat", () => ({
  useChat: () => ({
    addQuestion: (...params: unknown[]) => addQuestionMock(...params),
    generatingAnswer: false,
  }),
}));

afterEach(() => {
  addQuestionMock.mockClear();
});

describe("ChatInput", () => {
  it("should render correctly", () => {
    // Rendering the ChatInput component
    const { getByTestId } = render(<ChatInput />);

    const chatInputForm = getByTestId("chat-input-form");
    expect(chatInputForm).toBeDefined();

    const chatInput = getByTestId("chat-input");
    expect(chatInput).toBeDefined();

    const submitButton = getByTestId("submit-button");
    expect(submitButton).toBeDefined();

    const configButton = getByTestId("config-button");
    expect(configButton).toBeDefined();

    const micButton = getByTestId("mic-button");
    expect(micButton).toBeDefined();
  });

  it("should not call addQuestion on form submit when message is empty", () => {
    const { getByTestId } = render(<ChatInput />);
    const chatInputForm = getByTestId("chat-input-form");
    fireEvent.submit(chatInputForm);

    // Asserting that the addQuestion function was called with the expected arguments
    expect(addQuestionMock).not.toHaveBeenCalled();
  });

  it("should call addQuestion once on form submit when message is not empty", () => {
    const { getByTestId } = render(<ChatInput />);
    const chatInput = getByTestId("chat-input");
    fireEvent.change(chatInput, { target: { value: "Test question" } });
    const chatInputForm = getByTestId("chat-input-form");
    fireEvent.submit(chatInputForm);

    // Asserting that the addQuestion function was called with the expected arguments
    expect(addQuestionMock).toHaveBeenCalledTimes(1);
    expect(addQuestionMock).toHaveBeenCalledWith(
      "Test question",
      expect.any(Function)
    );
  });

  it('should submit a question when "Enter" key is pressed without shift', () => {
    // Mocking the addQuestion function

    // Rendering the ChatInput component with the mock function
    const { getByTestId } = render(<ChatInput />);
    const chatInput = getByTestId("chat-input");

    fireEvent.change(chatInput, { target: { value: "Another test question" } });
    fireEvent.keyDown(chatInput, { key: "Enter", shiftKey: false });

    // Asserting that the addQuestion function was called with the expected arguments
    expect(addQuestionMock).toHaveBeenCalledTimes(1);
    expect(addQuestionMock).toHaveBeenCalledWith(
      "Another test question",
      expect.any(Function)
    );
  });

  it('should not submit a question when "Enter" key is pressed with shift', () => {
    const { getByTestId } = render(<ChatInput />);

    const inputElement = getByTestId("chat-input");

    fireEvent.change(inputElement, { target: { value: "Test question" } });
    fireEvent.keyDown(inputElement, { key: "Enter", shiftKey: true });

    expect(addQuestionMock).not.toHaveBeenCalled();
  });
});
