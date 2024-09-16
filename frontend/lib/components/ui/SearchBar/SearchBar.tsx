import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";

import { ChatBar } from "../ChatBar/ChatBar";

export const SearchBar = ({
  onSearch,
  newBrain,
}: {
  onSearch?: () => void;
  newBrain?: boolean;
}): JSX.Element => {
  const chatInput = useChatInput();

  return <ChatBar onSearch={onSearch} newBrain={newBrain} {...chatInput} />;
};
