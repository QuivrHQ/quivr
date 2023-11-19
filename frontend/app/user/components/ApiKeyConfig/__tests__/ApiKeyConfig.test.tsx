import { fireEvent, render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiKeyConfig } from "../ApiKeyConfig";

const handleCreateClickMock = vi.fn(() => ({}));
const handleCopyClickMock = vi.fn(() => ({}));

const useApiKeyConfigMock = vi.fn(() => ({
  apiKey: "",
  handleCreateClick: () => handleCreateClickMock(),
  handleCopyClick: () => handleCopyClickMock(),
}));

vi.mock("../hooks/useApiKeyConfig", () => ({
  useApiKeyConfig: () => useApiKeyConfigMock(),
}));

describe("ApiKeyConfig", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should render ApiConfig Component", () => {
    const { getByTestId } = render(<ApiKeyConfig />);
    expect(getByTestId("create-new-key")).toBeDefined();
  });

  it("renders 'Create New Key' button when apiKey is empty", () => {
    const { getByTestId } = render(<ApiKeyConfig />);

    const createButton = getByTestId("create-new-key");
    expect(createButton).toBeDefined();

    fireEvent.click(createButton);
    expect(handleCreateClickMock).toHaveBeenCalledTimes(1);
    expect(handleCreateClickMock).toHaveBeenCalledWith();
  });
  it('renders "Copy" button when apiKey is not empty', () => {
    useApiKeyConfigMock.mockReturnValue({
      apiKey: "123456789",
      handleCreateClick: () => handleCreateClickMock(),
      handleCopyClick: () => handleCopyClickMock(),
    });

    const { getByTestId } = render(<ApiKeyConfig />);
    const copyButton = getByTestId("copy-api-key-button");
    expect(copyButton).toBeDefined();
    fireEvent.click(copyButton);
    expect(handleCopyClickMock).toHaveBeenCalledTimes(1);
  });
});
