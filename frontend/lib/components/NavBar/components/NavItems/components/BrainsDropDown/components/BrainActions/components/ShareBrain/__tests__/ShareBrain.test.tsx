import { fireEvent, render } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { ShareBrain } from "../ShareBrain";

describe("ShareBrain", () => {
  it("should render ShareBrain component properly", () => {
    const { getByTestId } = render(
      <ShareBrain brainId="cf9bb422-b1b6-4fd7-abc1-01bd395d2318" />
    );
    const shareButton = getByTestId("share-brain-button");
    expect(shareButton).toBeDefined();
  });

  it("should render open share modal when share button is clicked", () => {
    const { getByText, getByTestId } = render(
      <ShareBrain brainId="cf9bb422-b1b6-4fd7-abc1-01bd395d2318" />
    );
    const shareButton = getByTestId("share-brain-button");
    fireEvent.click(shareButton);
    expect(getByText("Share brain")).toBeDefined();
  });

  it('shoud add new user row when "Add new user" button is clicked and only where there is no empty field', async () => {
    const { getByTestId, findAllByTestId } = render(
      <ShareBrain brainId="cf9bb422-b1b6-4fd7-abc1-01bd395d2318" />
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
