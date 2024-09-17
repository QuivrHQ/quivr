import { iconList } from "@/lib/helpers/iconList";

export interface AssistantCardType {
  name: string;
  description: string;
  disabled?: boolean;
  iconName: keyof typeof iconList;
}
