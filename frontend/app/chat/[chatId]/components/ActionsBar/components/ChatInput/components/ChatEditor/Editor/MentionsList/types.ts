import { SuggestionData, SuggestionItem } from "../types";

export type MentionListProps = {
  suggestionData: SuggestionData;
  command: (item: SuggestionItem) => void;
};
