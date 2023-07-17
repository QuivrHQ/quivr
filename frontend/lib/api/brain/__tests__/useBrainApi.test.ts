/* eslint-disable max-lines */
import { renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useBrainApi } from "../useBrainApi";

const axiosGetMock = vi.fn(() => ({
  data: {
    documents: [],
  },
}));

const axiosPostMock = vi.fn(() => ({
  data: {
    id: "123",
    name: "Test Brain",
  },
}));

const axiosDeleteMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: vi.fn(() => ({
    axiosInstance: {
      get: axiosGetMock,
      post: axiosPostMock,
      delete: axiosDeleteMock,
    },
  })),
}));

describe("useBrainApi", () => {
  afterEach(() => {
    vi.restoreAllMocks();
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

  it("should call createBrain with the correct parameters", async () => {
    const {
      result: {
        current: { createBrain },
      },
    } = renderHook(() => useBrainApi());
    const name = "Test Brain";
    await createBrain(name);

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith("/brains/", { name });
  });

  it("should call deleteBrain with the correct parameters", async () => {
    const {
      result: {
        current: { deleteBrain },
      },
    } = renderHook(() => useBrainApi());
    const id = "123";
    await deleteBrain(id);

    expect(axiosDeleteMock).toHaveBeenCalledTimes(1);
    expect(axiosDeleteMock).toHaveBeenCalledWith(`/brain/${id}/subscription`);
  });

  it("should call getDefaultBrain with the correct parameters", async () => {
    const {
      result: {
        current: { getDefaultBrain },
      },
    } = renderHook(() => useBrainApi());
    await getDefaultBrain();

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith("/brains/default/");
  });

  it("should call getBrains with the correct parameters", async () => {
    const {
      result: {
        current: { getBrains },
      },
    } = renderHook(() => useBrainApi());
    await getBrains();

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith("/brains/");
  });

  it("should call getBrain with the correct parameters", async () => {
    const {
      result: {
        current: { getBrain },
      },
    } = renderHook(() => useBrainApi());
    const id = "123";
    await getBrain(id);

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/brains/${id}/`);
  });

  it("should call addBrainSubscription with the correct parameters", async () => {
    const {
      result: {
        current: { addBrainSubscriptions },
      },
    } = renderHook(() => useBrainApi());
    const id = "123";
    const subscriptions = [
      {
        email: "user@quivr.app",
        rights: "viewer",
      },
    ];
    await addBrainSubscriptions(id, subscriptions);

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith(
      `/brain/${id}/subscription`,
      subscriptions
    );
  });
});
