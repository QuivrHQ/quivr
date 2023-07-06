import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { useAuthApi } from "../useAuthApi";

const axiosPostMock = vi.fn(() => ({
  data: {
    api_key: "",
  },
}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      post: axiosPostMock,
    },
  }),
}));

describe("useAuthApi", () => {
  it("should call createApiKey with the correct parameters", async () => {
    const {
      result: {
        current: { createApiKey },
      },
    } = renderHook(() => useAuthApi());
    await createApiKey();
    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith("/api-key");
  });
});
