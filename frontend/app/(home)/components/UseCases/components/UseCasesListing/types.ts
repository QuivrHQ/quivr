export type UseCase = {
  id: string;
  name: string;
  description: string;
  discussions: {
    question: string;
    answer: string;
  }[];
};
