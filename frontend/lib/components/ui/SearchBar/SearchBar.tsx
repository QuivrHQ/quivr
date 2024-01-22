import { useEffect, useState } from "react";
import { LuSearch } from "react-icons/lu";

import { Editor } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/components/Editor/Editor";
import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useChatContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { LoaderIcon } from "../LoaderIcon/LoaderIcon";
// eslint-disable-next-line import/order
import styles from "./SearchBar.module.scss";

export const SearchBar = (): JSX.Element => {
  const [searching, setSearching] = useState(false);
  const { message, setMessage } = useChatInput();
  const { setMessages } = useChatContext();
  const { addQuestion } = useChat();
  const { setCurrentBrainId } = useBrainContext();

  useEffect(() => {
    setCurrentBrainId(null);
  });

  const submit = async (): Promise<void> => {
    setSearching(true);
    setMessages([]);
    try {
      await addQuestion(message);
    } catch (error) {
      console.error(error);
    } finally {
      setSearching(false);
    }
  };

  /* eslint-disable @typescript-eslint/restrict-template-expressions */

  return (
    <div className={styles.search_bar_wrapper}>
      <Editor
        message={message}
        setMessage={setMessage}
        onSubmit={() => void submit()}
        placeholder="Search"
      ></Editor>
      {searching ? (
        <LoaderIcon size="big" />
      ) : (
        <LuSearch
          className={`${styles.search_icon} ${!message ? styles.disabled : ""}`}
          onClick={() => void submit()}
        />
      )}
    </div>
  );
};
