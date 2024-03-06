"use client";

import { CurrentBrain } from "@/lib/components/CurrentBrain/CurrentBrain";
import Icon from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { ThreadEditor } from "./components/ThreadEditor/ThreadEditor";
import { useThreadInput } from "./hooks/useThreadInput";
import styles from "./index.module.scss";

export const ThreadInput = (): JSX.Element => {
  const { setMessage, submitQuestion, generatingAnswer, message } =
    useThreadInput();
  const { currentBrain } = useBrainContext();

  const handleSubmitQuestion = () => {
    if (message.trim() !== "") {
      submitQuestion();
    }
  };

  return (
    <>
      <form
        data-testid="thread-input-form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmitQuestion();
        }}
      >
        <div className={styles.thread_container}>
          <CurrentBrain allowingRemoveBrain={false} />
          <div
            className={`
            ${styles.thread_wrapper}
            ${currentBrain ? styles.with_brain : ""}
          `}
          >
            <ThreadEditor
              message={message}
              setMessage={setMessage}
              onSubmit={handleSubmitQuestion}
            />
            {generatingAnswer ? (
              <LoaderIcon size="large" color="accent" />
            ) : (
              <Icon
                name="followUp"
                size="large"
                color="accent"
                disabled={!message}
                handleHover={true}
                onClick={handleSubmitQuestion}
              />
            )}
          </div>
        </div>
      </form>
    </>
  );
};
