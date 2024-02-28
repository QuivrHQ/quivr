import { iconList } from "@/lib/helpers/iconList";

import { Color } from "./Colors";

export type Option = {
  label: string;
  iconName: keyof typeof iconList;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onClick: (object?: any) => void;
  iconColor: Color;
  disabled?: boolean;
};
