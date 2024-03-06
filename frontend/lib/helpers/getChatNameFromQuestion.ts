export const getThreadNameFromQuestion = (question: string): string =>
  question.split(" ").slice(0, 3).join(" ");
