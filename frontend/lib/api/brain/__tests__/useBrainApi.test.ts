/* eslint-disable max-lines */
import { renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Subscription } from "../brain";
import {
  CreateBrainInput,
  SubscriptionUpdatableProperties,
  UpdateBrainInput,
} from "../types";
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
const axiosPutMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: vi.fn(() => ({
    axiosInstance: {
      get: axiosGetMock,
      post: axiosPostMock,
      delete: axiosDeleteMock,
      put: axiosPutMock,
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

    const brain: CreateBrainInput = {
      name: "Test Brain",
      description: "This is a description",
      status: "public",
      model: "gpt-3.5-turbo",
      temperature: 0.0,
      max_tokens: 256,
      openai_api_key: "123",
    };

    await createBrain(brain);

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith("/brains/", brain);
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
    expect(axiosDeleteMock).toHaveBeenCalledWith(`/brains/${id}/subscription`);
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
    axiosGetMock.mockImplementationOnce(() => ({
      data: {
        //@ts-ignore we don't really need returned value here
        brains: [],
      },
    }));
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
    const subscriptions: Subscription[] = [
      {
        email: "user@quivr.app",
        role: "Viewer",
      },
    ];
    await addBrainSubscriptions(id, subscriptions);

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith(`/brains/${id}/subscription`, [
      {
        email: "user@quivr.app",
        rights: "Viewer",
      },
    ]);
  });

  it("should call getBrainUsers with the correct parameters", async () => {
    axiosGetMock.mockImplementationOnce(() => ({
      //@ts-ignore we don't really need returned value here
      data: [],
    }));

    const {
      result: {
        current: { getBrainUsers },
      },
    } = renderHook(() => useBrainApi());
    const id = "123";
    await getBrainUsers(id);

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/brains/${id}/users`);
  });
  it("should call updateBrainAccess with the correct parameters", async () => {
    const {
      result: {
        current: { updateBrainAccess },
      },
    } = renderHook(() => useBrainApi());
    const brainId = "123";
    const email = "456";
    const subscription: SubscriptionUpdatableProperties = {
      role: "Viewer",
    };
    await updateBrainAccess(brainId, email, subscription);
    expect(axiosPutMock).toHaveBeenCalledTimes(1);
    expect(axiosPutMock).toHaveBeenCalledWith(
      `/brains/${brainId}/subscription`,
      { rights: "Viewer", email }
    );
  });

  it("should call setAsDefaultBrain with correct brainId", async () => {
    const {
      result: {
        current: { setAsDefaultBrain },
      },
    } = renderHook(() => useBrainApi());
    const brainId = "123";
    await setAsDefaultBrain(brainId);
    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith(`/brains/${brainId}/default`);
  });

  it("should call updateBrain with correct brainId and brain", async () => {
    const {
      result: {
        current: { updateBrain },
      },
    } = renderHook(() => useBrainApi());
    const brainId = "123";
    const brain: UpdateBrainInput = {
      name: "Test Brain",
      description: "This is a description",
      status: "public",
      model: "gpt-3.5-turbo",
      temperature: 0.0,
      max_tokens: 256,
      openai_api_key: "123",
    };
    await updateBrain(brainId, brain);
    expect(axiosPutMock).toHaveBeenCalledTimes(1);
    expect(axiosPutMock).toHaveBeenCalledWith(`/brains/${brainId}/`, brain);
  });
  it("should call getPublicBrains with correct parameters", async () => {
    const {
      result: {
        current: { getPublicBrains },
      },
    } = renderHook(() => useBrainApi());
    await getPublicBrains();
    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/brains/public`);
  });
});
