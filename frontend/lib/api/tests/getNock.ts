import nock from "nock";
import { vi } from "vitest";

import { DEFAULT_BACKEND_URL } from "@/lib/config/CONSTANTS";

vi.mock("@/lib/context/SupabaseProvider", () => ({
  useSupabase: () => ({}),
}));

export const getNock = (url?: string): nock.Scope => {
  return nock(
    url ?? `${process.env.NEXT_PUBLIC_BACKEND_URL ?? DEFAULT_BACKEND_URL}`
  ).defaultReplyHeaders({
    "access-control-allow-origin": "*",
    "access-control-allow-credentials": "true",
    "access-control-allow-headers": "Authorization",
  });
};
