type Discussion = {
  question: string;
  answer: string;
};

export type UseCase = {
  id: string;
  name: string;
  description: string;
  discussions: Discussion[];
};
