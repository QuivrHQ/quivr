/* eslint-disable max-lines */
import { act, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { Sidebar } from "@/lib/components/Sidebar/Sidebar";

describe("Sidebar", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("is rendered by default on desktop", async () => {
    vi.mock("@/lib/hooks/useDevice", () => ({
      useDevice: () => ({ isMobile: false }),
    }));

    await act(() =>
      render(
        <Sidebar showFooter={false}>
          <div data-testid="sidebar-test-content">📦</div>
        </Sidebar>
      )
    );

    const closeSidebarButton = screen.queryByTestId("close-sidebar-button");
    expect(closeSidebarButton).toBeVisible();

    // FIXME: this is not working
    // const openSidebarButton = screen.queryByTestId("open-sidebar-button");
    // expect(openSidebarButton).not.toBeVisible();

    const sidebarContent = screen.getByTestId("sidebar-test-content");
    expect(sidebarContent).toBeVisible();
  });

  it("is hidden by default on mobile", async () => {
    vi.mock("@/lib/hooks/useDevice", () => ({
      useDevice: () => ({ isMobile: true }),
    }));

    await act(() =>
      render(
        <Sidebar showFooter={false}>
          <div data-testid="sidebar-test-content">📦</div>
        </Sidebar>
      )
    );

    const closeSidebarButton = screen.queryByTestId("close-sidebar-button");
    expect(closeSidebarButton).not.toBeVisible();
    const openSidebarButton = screen.queryByTestId("open-sidebar-button");
    expect(openSidebarButton).toBeVisible();

    const sidebarContent = screen.getByTestId("sidebar-test-content");
    expect(sidebarContent).not.toBeVisible();
  });

  // TODO: test open/close buttons
});
