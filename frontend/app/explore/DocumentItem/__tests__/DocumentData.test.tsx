import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { BrainConfigProvider } from "@/lib/context/BrainConfigProvider";

import DocumentData from "../DocumentData";

const useSupabaseMock = vi.fn(() => ({
  session: { user: {} },
}));

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => useSupabaseMock(),
}));

vi.mock("@/lib/hooks", async () => {
  const actual = await vi.importActual<typeof import("@/lib/hooks")>(
    "@/lib/hooks"
  );

  return {
    ...actual,
    useAxios: () => ({
      axiosInstance: {
        get: vi.fn().mockResolvedValue({
          data: {
            documents: [
              {
                file_name: "mock_file_name.pdf",
                file_size: "0",
                file_extension: null,
                file_url: null,
                content: "foo,bar\nbaz,bat",
                brains_vectors: [
                  {
                    brain_id: "mock_brain_id",
                    vector_id: "mock_vector_id_1",
                  },
                ],
              },
              {
                file_name: "mock_file_name.pdf",
                file_size: "0",
                file_extension: null,
                file_url: null,
                content: "foo,bar\nbaz,bat",
                brains_vectors: [
                  {
                    brain_id: "mock_brain_id",
                    vector_id: "mock_vector_id_2",
                  },
                ],
              },
            ],
          },
        }),
      },
    }),
  };
});

describe("DocumentData", () => {
  it("should render document data", async () => {
    const documentName = "Test document";
    render(
      <BrainConfigProvider>
        <DocumentData documentName={documentName} />
      </BrainConfigProvider>
    );

    expect(screen.getByText(documentName)).toBeDefined();

    await waitFor(() => {
      expect(screen.getByText("content")).toBeDefined();
      expect(screen.getByText("foo,bar", { exact: false })).toBeDefined();
      expect(screen.getByText("baz,bat", { exact: false })).toBeDefined();
    });
  });
});
