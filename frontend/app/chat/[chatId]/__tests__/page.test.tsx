import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import {
  BrainConfigContextMock,
  BrainConfigProviderMock,
} from "@/lib/context/BrainConfigProvider/mocks/BrainConfigProviderMock";
import {
  BrainContextMock,
  BrainProviderMock,
} from "@/lib/context/BrainProvider/mocks/BrainProviderMock";
import {
  ChatContextMock,
  ChatProviderMock,
} from "@/lib/context/ChatProvider/mocks/ChatProviderMock";
import {
  SupabaseContextMock,
  SupabaseProviderMock,
} from "@/lib/context/SupabaseProvider/mocks/SupabaseProviderMock";

import SelectedChatPage from "../page";

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

vi.mock("@/lib/context/BrainConfigProvider/brain-config-provider", () => ({
  BrainConfigContext: BrainConfigContextMock,
}));

describe("Chat page", () => {
  it("should render chat page correctly", () => {
    const { getByTestId } = render(
      <ChatProviderMock>
        <SupabaseProviderMock>
          <BrainConfigProviderMock>
            <BrainProviderMock>
              <SelectedChatPage />,
            </BrainProviderMock>
          </BrainConfigProviderMock>
        </SupabaseProviderMock>
      </ChatProviderMock>
    );

    expect(getByTestId("chat-page")).toBeDefined();
    expect(getByTestId("chat-input")).toBeDefined();
  });
});
