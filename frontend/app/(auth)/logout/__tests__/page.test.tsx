import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import Logout from "../page";

// mocking related hooks
const mockUseLogout = vi.fn(() => ({
  handleLogout: vi.fn(),
  isPending: false,
}));

vi.mock("../hooks/useLogout", () => ({
  useLogout: () => mockUseLogout(),
}));

describe("Logout component", () => {
  it("should render correctly", () => {
    const { getByTestId } = render(<Logout />);
    const logoutPage = getByTestId("logout-page");
    expect(logoutPage).toBeDefined();
  });

  it("should call handleLogout 1 time when logout button is clicked", () => {
    const mockHandleLogout = vi.fn();

    mockUseLogout.mockReturnValue({
      handleLogout: mockHandleLogout,
      isPending: false,
    });

    const { getByTestId } = render(<Logout />);
    const logoutButton = getByTestId("logout-button");
    logoutButton.click();

    expect(mockHandleLogout).toHaveBeenCalledTimes(1);
  });

  it("should not call handleLogout when isPending is true", () => {
    const mockHandleLogout = vi.fn();

    mockUseLogout.mockReturnValue({
      handleLogout: mockHandleLogout,
      isPending: true,
    });

    const { getByTestId } = render(<Logout />);
    const logoutButton = getByTestId("logout-button");
    logoutButton.click();
    expect(mockHandleLogout).toHaveBeenCalledTimes(0);
  });
});
