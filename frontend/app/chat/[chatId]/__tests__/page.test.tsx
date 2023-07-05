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
    const { getByTestId, getByText } = render(
      <SupabaseProviderMock>
        <BrainConfigProviderMock>
          <BrainProviderMock>
            <SelectedChatPage />,
          </BrainProviderMock>
        </BrainConfigProviderMock>
      </SupabaseProviderMock>
    );

    expect(getByTestId("chat-page")).toBeDefined();
    expect(getByTestId("chat-messages")).toBeDefined();
    expect(getByTestId("chat-input")).toBeDefined();

    expect(getByText("Chat with your brain")).toBeDefined();
    expect(
      getByText("Talk to a language model about your uploaded data")
    ).toBeDefined();
  });
});
