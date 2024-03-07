import { iconList } from "../helpers/iconList";

export interface Tab {
  label: string;
  isSelected: boolean;
  disabled?: boolean;
  iconName: keyof typeof iconList;
  onClick: () => void;
}
