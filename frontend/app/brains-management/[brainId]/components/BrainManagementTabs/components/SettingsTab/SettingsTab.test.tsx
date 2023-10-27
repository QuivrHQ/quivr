import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import {
  BrainContextMock,
  BrainProviderMock,
} from "@/lib/context/BrainProvider/mocks/BrainProviderMock";
import {
  SupabaseContextMock,
  SupabaseProviderMock,
} from "@/lib/context/SupabaseProvider/mocks/SupabaseProviderMock";

import { SettingsTab } from "./SettingsTab";

const useTranslationMock = vi.fn(() => ({
  t: (str: string): string => str,
}));

vi.mock("react-i18next", () => ({
  useTranslation: () => useTranslationMock(),
}));

vi.mock("@/lib/context/SupabaseProvider/supabase-provider", () => ({
  SupabaseContext: SupabaseContextMock,
}));

vi.mock("@/lib/context/BrainProvider/brain-provider", () => ({
  BrainContext: BrainContextMock,
}));

vi.mock("@/lib/api/brain/useBrainApi", () => ({
  useBrainApi: () => ({
    setAsDefaultBrain: () => [],
    updateBrain: () => [],
  }),
}));

vi.mock("@tanstack/react-query", async () => {
  const actual = await vi.importActual<typeof import("@tanstack/react-query")>(
    "@tanstack/react-query"
  );

  vi.mock("next/navigation", () => ({
    useRouter: () => ({ replace: vi.fn() }),
  }));

  return {
    ...actual,
    useQuery: () => ({
      data: {},
    }),
  };
});

vi.mock("@/lib/hooks", async () => {
  const actual = await vi.importActual<typeof import("@/lib/hooks")>(
    "@/lib/hooks"
  );

  return {
    ...actual,
    useAxios: () => ({
      ...actual.useAxios(),
      axiosInstance: {
        get: vi.fn(() => ({
          data: [],
        })),
      },
    }),
  };
});

describe("Settings tab in brains-management", () => {
  it("should render the seettings tab correctly", () => {
    const brainId = "4adefe4e-eb08-4208-b237-";

    render(
      <SupabaseProviderMock>
        <BrainProviderMock>
          <SettingsTab brainId={brainId} />
        </BrainProviderMock>
      </SupabaseProviderMock>
    );

    expect(
      screen.getByRole("button", { name: "setDefaultBrain" })
    ).toBeVisible();
    expect(screen.getByText("brainName")).toBeVisible();
    expect(screen.getByLabelText("brainDescription")).toBeVisible();

    expect(screen.getByLabelText("promptName")).toBeVisible();
  });
});
2;
