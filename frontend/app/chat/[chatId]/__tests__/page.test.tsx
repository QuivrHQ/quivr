import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import {
  BrainContextMock,
  BrainProviderMock,
} from "@/lib/context/BrainProvider/mocks/BrainProviderMock";
import {
  ChatContextMock,
  ChatProviderMock,
} from "@/lib/context/ChatProvider/mocks/ChatProviderMock";
import { KnowledgeToFeedProvider } from "@/lib/context/KnowledgeToFeedProvider";
import {
  SupabaseContextMock,
  SupabaseProviderMock,
} from "@/lib/context/SupabaseProvider/mocks/SupabaseProviderMock";

import SelectedChatPage from "../page";

const queryClient = new QueryClient();

vi.mock("@/lib/context/ChatProvider/ChatProvider", () => ({
  ChatContext: ChatContextMock,
  ChatProvider: ChatProviderMock,
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({ replace: vi.fn() }),
  useParams: () => ({ chatId: "1" }),
}));

vi.mock("@/lib/context/SupabaseProvider/supabase-provider", () => ({
  SupabaseContext: SupabaseContextMock,
}));

vi.mock("@/lib/context/BrainProvider/brain-provider", () => ({
  BrainContext: BrainContextMock,
}));

vi.mock("@/lib/api/chat/useChatApi", () => ({
  useChatApi: () => ({
    getHistory: () => [],
  }),
}));

vi.mock("@/lib/hooks", async () => {
  const actual = await vi.importActual<typeof import("@/lib/hooks")>(
    "@/lib/hooks"
  );

  return {
    ...actual,
    useAxios: () => ({
      axiosInstance: {
        get: vi.fn(() => ({ data: [] })),
      },
    }),
  };
});

vi.mock("@tanstack/react-query", async () => {
  const actual = await vi.importActual<typeof import("@tanstack/react-query")>(
    "@tanstack/react-query"
  );

  return {
    ...actual,
    useQuery: () => ({
      data: {},
    }),
  };
});

describe("Chat page", () => {
  it("should render chat page correctly", () => {
    const { getByTestId } = render(
      <KnowledgeToFeedProvider>
        <QueryClientProvider client={queryClient}>
          <ChatProviderMock>
            <SupabaseProviderMock>
              <BrainProviderMock>
                <SelectedChatPage />,
              </BrainProviderMock>
            </SupabaseProviderMock>
          </ChatProviderMock>
        </QueryClientProvider>
      </KnowledgeToFeedProvider>
    );

    expect(getByTestId("chat-page")).toBeDefined();
    expect(getByTestId("chat-input")).toBeDefined();
  });
});
