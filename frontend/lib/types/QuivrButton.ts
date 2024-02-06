import { Color } from "./Colors";

export interface ButtonType {
  label: string;
  color: Color;
  isLoading?: boolean;
  onClick: () => void;
}
