import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { BackendConfig } from "../BackendConfig";

const registerMock = vi.fn(() => void 0);

describe("BackendConfig", () => {
  it("renders the component with fields and labels", () => {
    //@ts-expect-error we don't need registerMock to return all `register` keys
    const { getByText } = render(<BackendConfig register={registerMock} />);

    expect(getByText("Backend config")).toBeDefined();
    expect(getByText("Backend URL")).toBeDefined();
    expect(getByText("Supabase URL")).toBeDefined();
    expect(getByText("Supabase key")).toBeDefined();
    expect(getByText("Keep in local")).toBeDefined();
    expect(getByText("Keep in local")).toBeDefined();
    expect(registerMock).toHaveBeenCalledWith("backendUrl");
    expect(registerMock).toHaveBeenCalledWith("supabaseUrl");
    expect(registerMock).toHaveBeenCalledWith("supabaseKey");
    expect(registerMock).toHaveBeenCalledWith("backendUrl");
  });
});
