export const getChatNameFromQuestion = (question: string): string =>
  question.split(" ").slice(0, 3).join(" ");
