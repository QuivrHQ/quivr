import { renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { CreatePromptProps, PromptUpdatableProperties } from "../prompt";
import { usePromptApi } from "../usePromptApi";

const axiosPostMock = vi.fn(() => ({}));
const axiosGetMock = vi.fn(() => ({}));
const axiosPutMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      post: axiosPostMock,
      get: axiosGetMock,
      put: axiosPutMock,
    },
  }),
}));

describe("usePromptApi", () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  it("should call createPrompt with the correct parameters", async () => {
    const prompt: CreatePromptProps = {
      title: "Test Prompt",
      content: "Test Content",
    };
    axiosPostMock.mockReturnValue({ data: {} });
    const {
      result: {
        current: { createPrompt },
      },
    } = renderHook(() => usePromptApi());
    await createPrompt(prompt);

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith("/prompts", prompt);
  });
  it("should call getPrompt with the correct parameters", async () => {
    const promptId = "test-prompt-id";
    axiosGetMock.mockReturnValue({ data: {} });
    const {
      result: {
        current: { getPrompt },
      },
    } = renderHook(() => usePromptApi());

    await getPrompt(promptId);

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/prompts/${promptId}`);
  });
  it("should call updatePrompt with the correct parameters", async () => {
    const promptId = "test-prompt-id";
    const prompt: PromptUpdatableProperties = {
      title: "Test Prompt",
      content: "Test Content",
    };
    axiosPutMock.mockReturnValue({ data: {} });
    const {
      result: {
        current: { updatePrompt },
      },
    } = renderHook(() => usePromptApi());

    await updatePrompt(promptId, prompt);

    expect(axiosPutMock).toHaveBeenCalledTimes(1);
    expect(axiosPutMock).toHaveBeenCalledWith(`/prompts/${promptId}`, prompt);
  });
  it("should call getPublicPrompts with the correct parameters", async () => {
    axiosGetMock.mockReturnValue({ data: [] });
    const {
      result: {
        current: { getPublicPrompts },
      },
    } = renderHook(() => usePromptApi());

    await getPublicPrompts();

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith("/prompts");
  });
});
