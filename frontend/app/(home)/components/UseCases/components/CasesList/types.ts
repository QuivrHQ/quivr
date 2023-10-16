export type CaseType = {
  id: string;
  name: string;
  description: string;
  discussions: {
    user: string;
    quivr: string;
  }[];
};
