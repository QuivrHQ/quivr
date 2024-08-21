export type SuggestionDataType = "prompt" | "brain";

export type SuggestionItem = {
  id: string;
  label: string;
  iconUrl?: string;
  snippet_emoji?: string;
  snippet_color?: string;
};

export type SuggestionData = {
  type: SuggestionDataType;
  items: SuggestionItem[];
};
