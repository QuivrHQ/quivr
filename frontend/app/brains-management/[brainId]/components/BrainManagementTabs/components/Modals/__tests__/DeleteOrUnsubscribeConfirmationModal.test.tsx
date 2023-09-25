import { render } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { DeleteOrUnsubscribeConfirmationModal } from "../DeleteOrUnsubscribeConfirmationModal";

describe("DeleteOrUnsubscribeConfirmationModal", () => {
  const isOpen = true;
  const setOpen = vi.fn();
  const onDelete = vi.fn();

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("should render delete modal", () => {
    const { getByTestId } = render(
      <DeleteOrUnsubscribeConfirmationModal
        isOpen={isOpen}
        setOpen={setOpen}
        onConfirm={onDelete}
      />
    );
    expect(getByTestId("modal-description")).toBeDefined();
    expect(getByTestId("return-button")).toBeDefined();
    expect(getByTestId("delete-brain")).toBeDefined();
  });

  it("should call onDelete when delete-brain is clicked", () => {
    const { getByTestId } = render(
      <DeleteOrUnsubscribeConfirmationModal
        isOpen={isOpen}
        setOpen={setOpen}
        onConfirm={onDelete}
      />
    );

    getByTestId("delete-brain").click();
    expect(onDelete).toHaveBeenCalledTimes(1);
  });
});
