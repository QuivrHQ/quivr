import { render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { BrainConfigProvider } from "@/lib/context/BrainConfigProvider";

import ConfigPage from "../page";

//  Mocks ConfirmButton as JSX.Element

const ConfirmFormMock = vi.fn<[], JSX.Element>(() => <div />);

const ConfirmTitleMock = vi.fn(() => <div />);
const ApiKeyConfig = vi.fn(() => <div />);

const redirectMock = vi.fn((props: unknown) => ({ props }));

const useSupabaseMock = vi.fn(() => ({
  session: null,
}));

vi.mock("next/navigation", () => ({
  redirect: (props: unknown) => redirectMock(props),
  useRouter: vi.fn(() => ({
    redirect: redirectMock,
  })),
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => useSupabaseMock(),
}));

describe("ConfigPage", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should redirect to /login if session is null", () => {
    render(
      <BrainConfigProvider>
        <ConfigPage />
      </BrainConfigProvider>
    );

    expect(redirectMock).toHaveBeenCalledTimes(1);
    expect(redirectMock).toHaveBeenCalledWith("/login");
  });

  it("should render config page if user is connected", () => {
    useSupabaseMock.mockReturnValue({
      // @ts-ignore we don't actually need parameters
      session: {
        user: {},
      },
    });

    vi.mock("../components", () => ({
      ConfigForm: () => ConfirmFormMock(),
      ConfigTitle: () => ConfirmTitleMock(),
      ApiKeyConfig: () => ApiKeyConfig(),
    }));

    render(
      <BrainConfigProvider>
        <ConfigPage />
      </BrainConfigProvider>
    );

    expect(redirectMock).not.toHaveBeenCalled();
    expect(ConfirmTitleMock).toHaveBeenCalledTimes(1);
    expect(ConfirmFormMock).toHaveBeenCalledTimes(1);
    expect(ApiKeyConfig).toHaveBeenCalledTimes(1);
  });
});
