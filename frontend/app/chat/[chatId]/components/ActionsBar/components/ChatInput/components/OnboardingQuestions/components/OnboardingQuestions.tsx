type OnboardingQuestionsProps = {
  question: string;
};

export const OnboardingQuestion = ({
  question,
}: OnboardingQuestionsProps): JSX.Element => {
  return (
    <div className="cursor-pointer shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow bg-yellow-100 px-3 py-1 rounded-xl border-black/10 dark:border-white/25">
      {question}
    </div>
  );
};
