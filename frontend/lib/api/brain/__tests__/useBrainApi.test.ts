import { renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useBrainApi } from "../useBrainApi";

const axiosGetMock = vi.fn(() => ({
  data: {
    documents: [],
  },
}));

vi.mock("@/lib/hooks", () => ({
  useAxios: vi.fn(() => ({
    axiosInstance: {
      get: axiosGetMock,
    },
  })),
}));

describe("useBrainApi", () => {
  afterEach(() => {
    vi.resetAllMocks();
  });

  it("should call getBrainDocuments with the correct parameters", async () => {
    const {
      result: {
        current: { getBrainDocuments },
      },
    } = renderHook(() => useBrainApi());
    const brainId = "123";
    await getBrainDocuments(brainId);

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/explore/?brain_id=${brainId}`);
  });
});
