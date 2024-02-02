import { useEffect, useState } from "react";
import { LuSearch } from "react-icons/lu";

import { Editor } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/components/Editor/Editor";
import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useChatContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./SearchBar.module.scss";

import { Icon } from "../Icon/Icon";
import { LoaderIcon } from "../LoaderIcon/LoaderIcon";

export const SearchBar = ({
  onSearch,
}: {
  onSearch?: () => void;
}): JSX.Element => {
  const [searching, setSearching] = useState(false);
  const [isDisabled, setIsDisabled] = useState(true);
  const { message, setMessage } = useChatInput();
  const { setMessages } = useChatContext();
  const { addQuestion } = useChat();
  const { currentBrain, setCurrentBrainId } = useBrainContext();

  useEffect(() => {
    setCurrentBrainId(null);
  }, []);

  useEffect(() => {
    setIsDisabled(message === "");
  }, [message]);

  const submit = async (): Promise<void> => {
    if (!searching) {
      setSearching(true);
      setMessages([]);
      try {
        if (onSearch) {
          onSearch();
        }
        await addQuestion(message);
      } catch (error) {
        console.error(error);
      } finally {
        setSearching(false);
      }
    }
  };

  const removeCurrentBrain = (): void => {
    setCurrentBrainId(null);
  };

  /* eslint-disable @typescript-eslint/restrict-template-expressions */
  return (
    <div
      className={`
      ${styles.search_bar_wrapper}
      ${currentBrain ? styles.with_brain : ""}`}
    >
      {currentBrain && (
        <div className={styles.current_brain_wrapper}>
          <div className={styles.brain_infos}>
            <div className={styles.left}>
              <span>Talking to</span>
              <div className={styles.brain_name_wrapper}>
                <Icon size="small" name="brain" color="primary" />
                <span className={styles.brain_name}>{currentBrain.name}</span>
              </div>
            </div>
            <div
              onClick={(event) => {
                event.nativeEvent.stopImmediatePropagation();
                removeCurrentBrain();
              }}
            >
              <Icon
                size="normal"
                name="close"
                color="black"
                handleHover={true}
              />
            </div>
          </div>
        </div>
      )}
      <div
        className={`
      ${styles.editor_wrapper}
      ${currentBrain ? styles.with_brain : ""}
      `}
      >
        <Editor
          message={message}
          setMessage={setMessage}
          onSubmit={() => void submit()}
          placeholder="Search"
        ></Editor>
        {searching ? (
          <LoaderIcon size="big" color="accent" />
        ) : (
          <LuSearch
            className={`
          ${styles.search_icon} 
          ${isDisabled ? styles.disabled : ""}
          `}
            onClick={() => void submit()}
          />
        )}
      </div>
    </div>
  );
};
