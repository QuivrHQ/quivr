import { fireEvent, render } from "@testing-library/react";
import sample from "lodash/sample";
import { afterEach, describe, expect, it, vi } from "vitest";

import LanguageSelect from "../LanguageSelect";
import { languages } from "../hooks/useLanguageHook";

const mockUseSupabase = vi.fn(() => ({
  supabase: {
    auth: {
      updateUser: vi.fn(),
    },
  },
  session: {
    user: {},
  },
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => mockUseSupabase(),
}));

const useTranslationMock = vi.fn(() => ({
  t: (str: string): string => str,
  i18n: {
    changeLanguage: (str: string) => str,
  },
}));

vi.mock("react-i18next", () => ({
  useTranslation: () => useTranslationMock(),
}));

const changeMock = vi.fn((str: string) => str);

vi.mock("useLanguage", () => ({
  change: changeMock,
  allLanguages: languages,
  currentLanguage: "en",
}));

vi.mock("@/services/analytics/june/useEventTracking", () => ({
  useEventTracking: () => ({ track: vi.fn() }),
}));

describe("LanguageSelect", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should render LanguageSelect component", () => {
    const { getByTestId } = render(<LanguageSelect />);
    const select = getByTestId("language-select");
    expect(select).toBeDefined();

    // defaults to light
    const options = select.getElementsByTagName("option");
    expect(options.length).toBeGreaterThan(0);
  });

  it("should select a language", () => {
    const { getByTestId } = render(<LanguageSelect />);
    const select = getByTestId("language-select");
    expect(select).toBeDefined();

    const choice = sample(Object.keys(languages)) as string;

    fireEvent.change(select, { target: { value: choice } });

    const selectedOption = getByTestId(`option-${choice}`) as HTMLOptionElement;

    expect(selectedOption.value).toBe(choice);
  });
});
