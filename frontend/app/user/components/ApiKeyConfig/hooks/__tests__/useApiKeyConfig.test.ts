import { act, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useApiKeyConfig } from "../useApiKeyConfig";

const createApiKeyMock = vi.fn(() => "dummyApiKey");
const trackMock = vi.fn((props: unknown) => ({ props }));

const useAuthApiMock = vi.fn(() => ({
  createApiKey: () => createApiKeyMock(),
}));

const useEventTrackingMock = vi.fn(() => ({
  track: (props: unknown) => trackMock(props),
}));

vi.mock("@/lib/api/auth/useAuthApi", () => ({
  useAuthApi: () => useAuthApiMock(),
}));
vi.mock("@/services/analytics/useEventTracking", () => ({
  useEventTracking: () => useEventTrackingMock(),
}));

describe("useApiKeyConfig", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should set the apiKey when handleCreateClick is called", async () => {
    const { result } = renderHook(() => useApiKeyConfig());

    await act(async () => {
      await result.current.handleCreateClick();
    });

    expect(createApiKeyMock).toHaveBeenCalledTimes(1);
    expect(trackMock).toHaveBeenCalledWith("CREATE_API_KEY");
    expect(result.current.apiKey).toBe("dummyApiKey");
  });

  it("should call copyToClipboard when handleCopyClick is called with a non-empty apiKey", () => {
    vi.mock("react", async () => {
      const actual = await vi.importActual<typeof import("react")>("react");

      return {
        ...actual,
        useState: () => ["dummyApiKey", vi.fn()],
      };
    });
    //@ts-ignore - clipboard is not actually readonly
    global.navigator.clipboard = {
      writeText: vi.fn(),
    };

    const { result } = renderHook(() => useApiKeyConfig());

    act(() => result.current.handleCopyClick());

    expect(trackMock).toHaveBeenCalledTimes(1);
    expect(trackMock).toHaveBeenCalledWith("COPY_API_KEY");

    // eslint-disable-next-line @typescript-eslint/unbound-method
    expect(global.navigator.clipboard.writeText).toHaveBeenCalledWith(
      "dummyApiKey"
    );
  });
});
