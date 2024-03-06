import { useEffect, useState } from "react";
import { LuSearch } from "react-icons/lu";

import { Editor } from "@/app/thread/[threadId]/components/ActionsBar/components/ThreadInput/components/ThreadEditor/Editor/Editor";
import { useThreadInput } from "@/app/thread/[threadId]/components/ActionsBar/components/ThreadInput/hooks/useChatInput";
import { useThread } from "@/app/thread/[threadId]/hooks/useThread";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useThreadContext } from "@/lib/context/ThreadProvider";

import styles from "./SearchBar.module.scss";

import { CurrentBrain } from "../../CurrentBrain/CurrentBrain";
import { LoaderIcon } from "../LoaderIcon/LoaderIcon";

export const SearchBar = ({
  onSearch,
}: {
  onSearch?: () => void;
}): JSX.Element => {
  const [searching, setSearching] = useState(false);
  const [isDisabled, setIsDisabled] = useState(true);
  const { message, setMessage } = useThreadInput();
  const { setMessages } = useThreadContext();
  const { addQuestion } = useThread();
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

  return (
    <div
      className={`
      ${styles.search_bar_wrapper}
      ${currentBrain ? styles.with_brain : ""}
      `}
    >
      <CurrentBrain allowingRemoveBrain={true} />
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
