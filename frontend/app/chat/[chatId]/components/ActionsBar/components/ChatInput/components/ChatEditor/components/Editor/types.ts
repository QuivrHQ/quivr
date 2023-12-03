export type SuggestionDataType = "prompt" | "brain";

export type SuggestionItem = {
  id: string;
  label: string;
};

export type SuggestionData = {
  type: SuggestionDataType;
  items: SuggestionItem[];
};
