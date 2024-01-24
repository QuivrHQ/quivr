import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { IconType } from "react-icons/lib";
import {
  LuBrain,
  LuChevronDown,
  LuChevronRight,
  LuPlusCircle,
  LuSearch,
} from "react-icons/lu";

export const iconList: { [name: string]: IconType } = {
  add: LuPlusCircle,
  brain: LuBrain,
  chevronDown: LuChevronDown,
  chevronRight: LuChevronRight,
  loader: AiOutlineLoading3Quarters,
  search: LuSearch,
};
