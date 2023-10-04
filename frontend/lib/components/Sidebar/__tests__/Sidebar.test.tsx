/* eslint-disable max-lines */
import {
  act,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Sidebar } from "@/lib/components/Sidebar/Sidebar";
import { useDevice } from "@/lib/hooks/useDevice";

vi.mock("@/lib/hooks/useDevice");

const renderSidebar = async () => {
  await act(() =>
    render(
      <Sidebar>
        <div data-testid="sidebar-test-content">📦</div>
      </Sidebar>
    )
  );
};

describe("Sidebar", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("is rendered by default on desktop", async () => {
    vi.mocked(useDevice).mockReturnValue({ isMobile: false });

    await renderSidebar();

    const closeSidebarButton = screen.queryByTestId("close-sidebar-button");
    expect(closeSidebarButton).toBeVisible();

    const sidebarContent = screen.getByTestId("sidebar-test-content");
    expect(sidebarContent).toBeVisible();
  });

  it("is hidden by default on mobile", async () => {
    vi.mocked(useDevice).mockReturnValue({ isMobile: true });

    await renderSidebar();

    const closeSidebarButton = screen.queryByTestId("close-sidebar-button");
    expect(closeSidebarButton).not.toBeVisible();
    const openSidebarButton = screen.queryByTestId("open-sidebar-button");
    expect(openSidebarButton).toBeVisible();

    const sidebarContent = screen.getByTestId("sidebar-test-content");
    expect(sidebarContent).not.toBeVisible();
  });

  it("shows and hide content when the open and close buttons are clicked", async () => {
    vi.mocked(useDevice).mockReturnValue({ isMobile: true });

    await renderSidebar();

    const openSidebarButton = screen.getByTestId("open-sidebar-button");
    expect(openSidebarButton).toBeVisible();

    const sidebarContent = screen.queryByTestId("sidebar-test-content");
    expect(sidebarContent).not.toBeVisible();

    fireEvent.click(openSidebarButton);

    await waitFor(() => expect(sidebarContent).toBeVisible());

    const closeSidebarButton = screen.getByTestId("close-sidebar-button");
    expect(closeSidebarButton);

    fireEvent.click(closeSidebarButton);
    await waitFor(() => expect(sidebarContent).not.toBeVisible());
  });
});
