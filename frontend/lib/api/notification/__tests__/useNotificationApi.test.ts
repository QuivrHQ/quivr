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
  it("should call getThreadNotifications with the correct parameters", async () => {
    const threadId = "test-thread-id";
    const {
      result: {
        current: { getThreadNotifications },
      },
    } = renderHook(() => useNotificationApi());
    await getThreadNotifications(threadId);
    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/notifications/${threadId}`);
  });
});
