import { render } from "@testing-library/react";
import { BrainConfigProviderMock } from "../context/BrainConfigProvider/mocks/BrainConfigProviderMock";
import { BrainProviderMock } from "../context/BrainProvider/mocks/BrainProviderMock";
import { ChatProviderMock } from "../context/ChatProvider/mocks/ChatProviderMock";
import { SupabaseProviderMock } from "../context/SupabaseProvider/mocks/SupabaseProviderMock";

export const renderWithMockContexts = (component: JSX.Element) => {
  return render(
    <SupabaseProviderMock>
      <BrainConfigProviderMock>
        <ChatProviderMock>
          <BrainProviderMock>{component}</BrainProviderMock>
        </ChatProviderMock>
      </BrainConfigProviderMock>
    </SupabaseProviderMock>
  );
};
