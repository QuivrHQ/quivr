import { renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { CrawlInputProps } from "../crawl";
import { useCrawlApi } from "../useCrawlApi";

const axiosPostMock = vi.fn(() => ({}));

vi.mock("@/lib/hooks", () => ({
  useAxios: () => ({
    axiosInstance: {
      post: axiosPostMock,
    },
  }),
}));

describe("useCrawlApi", () => {
  // TODO: Create a test user within preview and prod databases to interact with
  it("should call updateUserIdentity with the correct parameters", async () => {
    const {
      result: {
        current: { crawlWebsiteUrl },
      },
    } = renderHook(() => useCrawlApi());
    const crawlInputProps: CrawlInputProps = {
      brainId: "e7001ccd-6d90-4eab-8c50-2f23d39441e4",
      chat_id: "e7001ccd-6d90-4eab-8c50-2f23d39441es",
      config: {
        url: "https://en.wikipedia.org/wiki/Mali",
        js: false,
        depth: 1,
        max_pages: 100,
        max_time: 60,
      },
    };
    await crawlWebsiteUrl(crawlInputProps);

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
    expect(axiosPostMock).toHaveBeenCalledWith(
      `/crawl?brain_id=${crawlInputProps.brainId}&chat_id=${
        crawlInputProps.chat_id ?? ""
      }`,
      crawlInputProps.config
    );
  });
});
