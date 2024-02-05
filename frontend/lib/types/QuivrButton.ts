import { Color } from "./Colors";

export interface Button {
  label: string;
  color: Color;
  onClick: () => void;
}
