import { AiOutlineLoading3Quarters } from "react-icons/ai";
import {
  FaCheck,
  FaCheckCircle,
  FaRegStar,
  FaRegUserCircle,
} from "react-icons/fa";
import { FaArrowUpFromBracket } from "react-icons/fa6";
import { IoHomeOutline } from "react-icons/io5";
import { IconType } from "react-icons/lib";
import {
  LuBrain,
  LuBrainCircuit,
  LuChevronDown,
  LuChevronRight,
  LuCopy,
  LuFile,
  LuPlus,
  LuPlusCircle,
  LuSearch,
} from "react-icons/lu";
import { MdDelete, MdEdit, MdHistory, MdUploadFile } from "react-icons/md";
import { RiHashtag } from "react-icons/ri";

export const iconList: { [name: string]: IconType } = {
  add: LuPlusCircle,
  addWithoutCircle: LuPlus,
  brain: LuBrain,
  brainCircuit: LuBrainCircuit,
  check: FaCheck,
  checkCircle: FaCheckCircle,
  chevronDown: LuChevronDown,
  chevronRight: LuChevronRight,
  copy: LuCopy,
  delete: MdDelete,
  edit: MdEdit,
  file: LuFile,
  followUp: FaArrowUpFromBracket,
  hastag: RiHashtag,
  history: MdHistory,
  home: IoHomeOutline,
  loader: AiOutlineLoading3Quarters,
  search: LuSearch,
  star: FaRegStar,
  upload: MdUploadFile,
  user: FaRegUserCircle,
};
