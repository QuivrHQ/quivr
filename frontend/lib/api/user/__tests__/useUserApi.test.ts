import { vi } from "vitest";


const axiosPutMock = vi.fn(() => ({}));
const axiosGetMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      put: axiosPutMock,
      get: axiosGetMock,
    },
  }),
}));

