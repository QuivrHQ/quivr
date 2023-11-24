"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
// import { useLanguageHook } from "@/app/user/components/LanguageDropDown/hooks/useLanguageHook";
import {
  getRandomQuestion,
  QUESTION_LIST_EN,
  QUESTION_LIST_ZH_CN,
  updateQuestion,
} from "@/lib/api/chat/utils";
import Button from "@/lib/components/ui/Button";

export const QuestionList = (): JSX.Element => {
  const { addQuestion, generatingAnswer } = useChat();
  const { setMessage } = useChatInput();

  const params = useParams();
  const [questions, setQuestions] = useState<string[]>([]);
  const [askingQuestion, setAskingQuestion] = useState<string>();
  const { i18n } = useTranslation();

  const chatId = (params?.chatId as string | undefined) ?? "";

  const generateBoardingChat = (question: string) => {
    if (!generatingAnswer) {
      setAskingQuestion(question);
      void addQuestion(question, () => {
        const updatedQuestions = updateQuestion(
          i18n.language,
          questions,
          question
        );
        setQuestions(updatedQuestions);
        setMessage("");
      });
    }
  };

  useEffect(() => {
    if (i18n.language === "en") {
      setQuestions(
        // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
        !chatId ? QUESTION_LIST_EN : getRandomQuestion(i18n.language, 3)
      );
    } else if (i18n.language === "zh_cn") {
      setQuestions(
        // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
        !chatId ? QUESTION_LIST_ZH_CN : getRandomQuestion(i18n.language, 3)
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [i18n.language]);

  return (
    <div className={`flex flex-wrap`}>
      {questions.length > 0 &&
        questions.map((question: string) => (
          <Button
            key={question}
            className="px-1 py-1 mb-1 mr-1 text-xs sm:text-sm"
            variant={"secondary"}
            isLoading={askingQuestion === question && generatingAnswer}
            onClick={() => void generateBoardingChat(question)}
          >
            {question}
          </Button>
        ))}
    </div>
  );
};
