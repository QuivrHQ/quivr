"use client";

import Icon from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import { OnboardingQuestions } from "./components";
import { ChatEditor } from "./components/ChatEditor/ChatEditor";
import { useChatInput } from "./hooks/useChatInput";

export const ChatInput = (): JSX.Element => {
  const { setMessage, submitQuestion, generatingAnswer, message } =
    useChatInput();

  const handleSubmitQuestion = () => {
    if (message.trim() !== "") {
      submitQuestion();
    }
  };

  return (
    <>
      <OnboardingQuestions />
      <div className="flex mt-1 flex-col w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-2">
        <form
          data-testid="chat-input-form"
          onSubmit={(e) => {
            e.preventDefault();
            handleSubmitQuestion();
          }}
          className="sticky bottom-0 bg-white dark:bg-black w-full flex items-center gap-2 z-20 p-2"
        >
          <div className="flex flex-1">
            <ChatEditor
              message={message}
              setMessage={setMessage}
              onSubmit={handleSubmitQuestion}
            />
          </div>
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
        </form>
      </div>
    </>
  );
};
