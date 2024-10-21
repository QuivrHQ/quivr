import { iconList } from "@/lib/helpers/iconList";

export interface BrainType {
  name: string;
  description: string;
  snippet_emoji: string;
  snippet_color: string;
  iconName: keyof typeof iconList;
  disabled?: boolean;
  onClick?: () => void;
}
