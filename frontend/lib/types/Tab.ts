import { iconList } from "../helpers/iconList";

export interface Tab {
  label: string;
  icon: keyof typeof iconList;
  isSelected: boolean;
  onClick: () => void;
}
