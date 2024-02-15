import { iconList } from "@/lib/helpers/iconList";

export type Option = {
  label: string;
  iconName: keyof typeof iconList;
  onClick: () => void;
};
