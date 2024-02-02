"use client";

import { CurrentBrain } from "@/lib/components/CurrentBrain/CurrentBrain";
import Icon from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { OnboardingQuestions } from "./components";
import { ChatEditor } from "./components/ChatEditor/ChatEditor";
import { useChatInput } from "./hooks/useChatInput";
import styles from "./index.module.scss";

export const ChatInput = (): JSX.Element => {
  const { setMessage, submitQuestion, generatingAnswer, message } =
    useChatInput();
  const { currentBrain } = useBrainContext();

  const handleSubmitQuestion = () => {
    if (message.trim() !== "") {
      submitQuestion();
    }
  };

  return (
    <>
      <OnboardingQuestions />

      <form
        data-testid="chat-input-form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSubmitQuestion();
        }}
      >
        <div className={styles.chat_container}>
          <CurrentBrain />
          <div
            className={`
            ${styles.chat_wrapper}
            ${currentBrain ? styles.with_brain : ""}
          `}
          >
            <ChatEditor
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
