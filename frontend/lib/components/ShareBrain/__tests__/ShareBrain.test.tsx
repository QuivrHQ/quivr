/* eslint-disable max-lines */
import { fireEvent, render } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  BrainContextMock,
  BrainProviderMock,
} from "@/lib/context/BrainProvider/mocks/BrainProviderMock";
import {
  SupabaseContextMock,
  SupabaseProviderMock,
} from "@/lib/context/SupabaseProvider/mocks/SupabaseProviderMock";

import { ShareBrain } from "../ShareBrain";

vi.mock("@/lib/context/SupabaseProvider/supabase-provider", () => ({
  SupabaseContext: SupabaseContextMock,
}));

vi.mock("@/lib/context/BrainProvider/brain-provider", () => ({
  BrainContext: BrainContextMock,
}));

vi.mock("@/lib/context/BrainProvider/hooks/useBrainContext", async () => {
  const actual = await vi.importActual<
    typeof import("@/lib/context/BrainProvider/hooks/useBrainContext")
  >("@/lib/context/BrainProvider/hooks/useBrainContext");

  return {
    ...actual,
    useBrainContext: () => ({
      ...actual.useBrainContext(),
      allBrains: [
        {
          id: "cf9bb422-b1b6-4fd7-abc1-01bd395d2318",
          name: "test",
          role: "Owner",
        },
      ],
      currentBrain: {
        role: "Editor",
      },
    }),
  };
});

vi.mock("@/lib/api/brain/useBrainApi", async () => {
  const actual = await vi.importActual<
    typeof import("@/lib/api/brain/useBrainApi")
  >("@/lib/api/brain/useBrainApi");

  return {
    ...actual,
    useBrainApi: () => ({
      ...actual.useBrainApi(),
      getBrainUsers: () => Promise.resolve([]),
    }),
  };
});

describe("ShareBrain", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("should render ShareBrain component properly", () => {
    const { getByTestId } = render(
      <SupabaseProviderMock>
        <BrainProviderMock>
          <ShareBrain brainId="cf9bb422-b1b6-4fd7-abc1-01bd395d2318" />
        </BrainProviderMock>
      </SupabaseProviderMock>
    );
    const shareButton = getByTestId("share-brain-button");
    expect(shareButton).toBeDefined();
  });

  it("should render open share modal when share button is clicked", () => {
    const { getByTestId } = render(
      // Todo: add a custom render function that wraps the component with the providers
      <SupabaseProviderMock>
        <BrainProviderMock>
          <ShareBrain brainId="cf9bb422-b1b6-4fd7-abc1-01bd395d2318" />
        </BrainProviderMock>
      </SupabaseProviderMock>
    );
    const shareButton = getByTestId("share-brain-button");
    fireEvent.click(shareButton);
    expect(getByTestId("modal-title")).toBeDefined();
  });

  it('shoud add new user row when "Add new user" button is clicked and only where there is no empty field', async () => {
    const { getByTestId, findAllByTestId } = render(
      <SupabaseProviderMock>
        <BrainProviderMock>
          <ShareBrain brainId="cf9bb422-b1b6-4fd7-abc1-01bd395d2318" />
        </BrainProviderMock>
      </SupabaseProviderMock>
    );
    const shareButton = getByTestId("share-brain-button");
    fireEvent.click(shareButton);

    let assignationRows = await findAllByTestId("assignation-row");

    expect(assignationRows.length).toBe(1);

    const firstAssignationRowEmailInput = (
      await findAllByTestId("role-assignation-email-input")
    )[0];

    fireEvent.change(firstAssignationRowEmailInput, {
      target: { value: "user@quivr.app" },
    });

    const addNewRoleAssignationButton = getByTestId("add-new-row-role-button");
    fireEvent.click(addNewRoleAssignationButton);

    assignationRows = await findAllByTestId("assignation-row");

    expect(assignationRows.length).toBe(2);
  });
});
