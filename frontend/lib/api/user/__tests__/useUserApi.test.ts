import { renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useUserApi } from "../useUserApi";
import { UserIdentityUpdatableProperties } from "../user";

const axiosPutMock = vi.fn(() => ({}));
const axiosGetMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      put: axiosPutMock,
      get: axiosGetMock,
    },
  }),
}));

describe("useUserApi", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });
  it("should call updateUserIdentity with the correct parameters", async () => {
    const {
      result: {
        current: { updateUserIdentity },
      },
    } = renderHook(() => useUserApi());
    const userUpdatableProperties: UserIdentityUpdatableProperties = {
      openai_api_key: "sk-xxx",
    };
    await updateUserIdentity(userUpdatableProperties);

    expect(axiosPutMock).toHaveBeenCalledTimes(1);
    expect(axiosPutMock).toHaveBeenCalledWith(
      `/user/identity`,
      userUpdatableProperties
    );
  });
  it("should call getUserIdentity with the correct parameters", async () => {
    const {
      result: {
        current: { getUserIdentity },
      },
    } = renderHook(() => useUserApi());
    await getUserIdentity();

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/user/identity`);
  });
  it("should call getUser with the correct parameters", async () => {
    const {
      result: {
        current: { getUser },
      },
    } = renderHook(() => useUserApi());
    await getUser();

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith(`/user`);
  });
});
