import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useNotificationApi } from "../useNotificationApi";

const axiosGetMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      get: axiosGetMock,
    },
  }),
}));

describe("useNotificationApi", () => {
  it("should call getChatNotifications with the correct parameters", async () => {
    const chatId = "test-chat-id";
    const {
      result: {
        current: { getChatNotifications },
      },
    } = renderHook(() => useNotificationApi());
    await getChatNotifications(chatId);
    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/notifications/${chatId}`);
  });
});
