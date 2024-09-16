import { forwardRef, useEffect, useState } from "react";
import { LuSearch } from "react-icons/lu";

import { Editor } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/components/ChatEditor/Editor/Editor";
import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChatContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./CharBar.module.scss";

import { CurrentBrain } from "../../CurrentBrain/CurrentBrain";
import { LoaderIcon } from "../LoaderIcon/LoaderIcon";

type ChatBarProps = {
  onSearch?: () => void;
  newBrain?: boolean;
} & ReturnType<typeof useChatInput>;

const ChatBar = forwardRef<HTMLDivElement, ChatBarProps>(
  (
    {
      onSearch,
      newBrain,
      message,
      setMessage,
      generatingAnswer,
      submitQuestion,
    },
    ref
  ): JSX.Element => {
    const [isDisabled, setIsDisabled] = useState(true);
    const [placeholder, setPlaceholder] = useState("Select a @brain");
    const { setMessages } = useChatContext();
    const { currentBrain, setCurrentBrainId } = useBrainContext();
    const { remainingCredits } = useUserSettingsContext();

    useEffect(() => {
      setCurrentBrainId(null);
    }, []);

    useEffect(() => {
      setIsDisabled(message === "");
    }, [message]);

    useEffect(() => {
      setPlaceholder(currentBrain ? "Ask a question..." : "Select a @brain");
    }, [currentBrain]);

    const submit = (): void => {
      if (!!remainingCredits && !!currentBrain && !generatingAnswer) {
        setMessages([]);
        try {
          if (onSearch) {
            onSearch();
          }
          submitQuestion(message);
        } catch (error) {
          console.error(error);
        }
      }
    };

    return (
      <div
        ref={ref}
        className={`${styles.search_bar_wrapper} ${
          newBrain ? styles.new_brain : ""
        }`}
      >
        <CurrentBrain
          allowingRemoveBrain={true}
          remainingCredits={remainingCredits}
          isNewBrain={newBrain}
        />
        <div
          className={`${styles.editor_wrapper} ${
            !remainingCredits ? styles.disabled : ""
          } ${currentBrain ? styles.current : ""}`}
        >
          <Editor
            message={message}
            setMessage={setMessage}
            onSubmit={() => submit()}
            placeholder={placeholder}
          ></Editor>
          {generatingAnswer ? (
            <LoaderIcon size="big" color="accent" />
          ) : (
            <LuSearch
              className={`
          ${styles.search_icon} 
          ${
            isDisabled || !remainingCredits || !currentBrain
              ? styles.disabled
              : ""
          }
          `}
              onClick={() => submit()}
            />
          )}
        </div>
      </div>
    );
  }
);

ChatBar.displayName = "ChatBar";

export { ChatBar };
