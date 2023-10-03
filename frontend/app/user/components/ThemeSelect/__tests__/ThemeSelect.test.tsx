import { fireEvent, render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import ThemeSelect from "../ThemeSelect";

const useTranslationMock = vi.fn(() => ({
  t: (str: string): string => str,
}));

vi.mock("react-i18next", () => ({
  useTranslation: () => useTranslationMock(),
}));

describe("ThemeSelect", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should render ThemeSelect component", () => {
    const { getByTestId } = render(<ThemeSelect />);
    const select = getByTestId("theme-select");
    expect(select).toBeDefined();
    expect(getByTestId("theme-dark")).toBeDefined();

    // defaults to light
    const lightOption = getByTestId("theme-light") as HTMLOptionElement;
    expect(lightOption).toBeDefined();
    expect(lightOption.selected).toBeTruthy();
  });

  it.each([
    { input: "dark", expected: { dark: true, light: false } },
    { input: "light", expected: { dark: false, light: true } },
  ])("should select $input theme option", ({ input, expected }) => {
    const { getByTestId } = render(<ThemeSelect />);
    const select = getByTestId("theme-select");
    const darkOption = getByTestId("theme-dark") as HTMLOptionElement;
    const lightOption = getByTestId("theme-light") as HTMLOptionElement;

    fireEvent.change(select, { target: { value: input } });

    expect(darkOption.selected).toBe(expected.dark);
    expect(lightOption.selected).toBe(expected.light);
  });
});
