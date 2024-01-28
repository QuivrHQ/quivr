import { AiOutlineLoading3Quarters } from "react-icons/ai";
import { FaCheckCircle, FaRegUserCircle } from "react-icons/fa";
import { FaArrowUpFromBracket } from "react-icons/fa6";
import { IconType } from "react-icons/lib";
import {
  LuBrain,
  LuChevronDown,
  LuChevronRight,
  LuCopy,
  LuPlusCircle,
  LuSearch,
} from "react-icons/lu";
import { RiHashtag } from "react-icons/ri";

export const iconList: { [name: string]: IconType } = {
  add: LuPlusCircle,
  brain: LuBrain,
  checkCircle: FaCheckCircle,
  chevronDown: LuChevronDown,
  chevronRight: LuChevronRight,
  copy: LuCopy,
  followUp: FaArrowUpFromBracket,
  hastag: RiHashtag,
  loader: AiOutlineLoading3Quarters,
  search: LuSearch,
  user: FaRegUserCircle,
};
