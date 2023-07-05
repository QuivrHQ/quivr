import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useChatApi } from "../useChatApi";

const axiosPostMock = vi.fn(() => ({}));
const axiosGetMock = vi.fn(() => ({}));
const axiosPutMock = vi.fn(() => ({}));
const axiosDeleteMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      post: axiosPostMock,
      get: axiosGetMock,
      put: axiosPutMock,
      delete: axiosDeleteMock,
    },
  }),
}));

describe("useChatApi", () => {
  it("should call createChat with the correct parameters", async () => {
    const chatName = "Test Chat";
    axiosPostMock.mockReturnValue({ data: {} });

    const {
      result: {
        current: { createChat },
      },
    } = renderHook(() => useChatApi());
    await createChat(chatName);

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith("/chat", {
      name: chatName,
    });
  });

  it("should call getChats with the correct parameters", async () => {
    axiosGetMock.mockReturnValue({ data: {} });
    const {
      result: {
        current: { getChats },
      },
    } = renderHook(() => useChatApi());

    await getChats();

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith("/chat");
  });

  it("should call deleteChat with the correct parameters", async () => {
    const chatId = "test-chat-id";
    axiosDeleteMock.mockReturnValue({});
    const {
      result: {
        current: { deleteChat },
      },
    } = renderHook(() => useChatApi());

    await deleteChat(chatId);

    expect(axiosDeleteMock).toHaveBeenCalledTimes(1);
    expect(axiosDeleteMock).toHaveBeenCalledWith(`/chat/${chatId}`);
  });
});
