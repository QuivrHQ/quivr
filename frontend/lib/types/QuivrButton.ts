import { Color } from "./Colors";

import { iconList } from "../helpers/iconList";

export interface ButtonType {
  label: string;
  color: Color;
  isLoading?: boolean;
  iconName: keyof typeof iconList;
  onClick?: () => void | Promise<void>;
  disabled?: boolean;
  hidden?: boolean;
  important?: boolean;
  small?: boolean;
}
