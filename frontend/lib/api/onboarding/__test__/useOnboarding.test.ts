import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { Onboarding } from "@/lib/types/Onboarding";

import { useOnboardingApi } from "../useOnboardingApi";

const axiosGetMock = vi.fn(() => ({}));
const axiosPutMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      get: axiosGetMock,
      put: axiosPutMock,
    },
  }),
}));

describe("useOnboarding", () => {
  it("should call getOnboarding with the correct parameters", async () => {
    axiosGetMock.mockReturnValue({ data: {} });
    const {
      result: {
        current: { getOnboarding },
      },
    } = renderHook(() => useOnboardingApi());

    await getOnboarding();

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith("/onboarding");
  });
  it("should call updateOnboarding with the correct parameters", async () => {
    const onboarding: Partial<Onboarding> = {
      onboarding_a: true,
      onboarding_b1: false,
    };
    axiosPutMock.mockReturnValue({ data: {} });
    const {
      result: {
        current: { updateOnboarding },
      },
    } = renderHook(() => useOnboardingApi());

    await updateOnboarding(onboarding);

    expect(axiosPutMock).toHaveBeenCalledTimes(1);
    expect(axiosPutMock).toHaveBeenCalledWith("/onboarding", onboarding);
  });
});
